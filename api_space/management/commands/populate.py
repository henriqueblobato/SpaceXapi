import datetime
from threading import Thread

from spaceXapi.settings import SPACECRAFT_FILE
from api_space.models import SpaceTrack, ObjectType, Country, Launch
from file_reader_tools.file_iterator import FileReader

from django.core.management.base import BaseCommand


def printt(obj, *args, **kwargs):
    print(*args, **kwargs)
    obj.stdout.write('Start populating DB')


def thread_task(func):
    def wrapper(*args, **kwargs):
        print('[{}] {} start'.format(datetime.datetime.now(), func.__name__))
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def flatten_data(d):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict):
            for k2, v2 in flatten_data(v).items():
                out[k2.lower()] = v2
        else:
            out[k] = v
    return out


def epoch_to_date_object(epoch):
    #  2020-10-13T02:56:59.566560
    date = datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)
    return date


def iso_to_date_object(iso):
    while True:
        for date_format in [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S.%f%z",
        ]:
            try:
                date = datetime.datetime.strptime(iso, date_format)
                tz_date = datetime.datetime(
                    date.year, date.month, date.day, date.hour, date.minute,
                    date.second, date.microsecond, tzinfo=datetime.timezone.utc
                )
                return tz_date
            except ValueError:
                continue
            except Exception as e:
                continue
        return None


class Command(BaseCommand):
    help = 'Reads a file specified in .env and populates the database with the data'

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='File to read', default=SPACECRAFT_FILE)

    def handle(self, *args, **options):

        printt(self, 'Start populating DB')
        file_name = options.get('file', SPACECRAFT_FILE)

        file_reader = FileReader()
        file_content = file_reader.json_file_iterator_with_progress_bar(filename=file_name)

        for space_track_info in file_content:
            try:
                space_track_info = flatten_data(space_track_info)

                obj_type, was_created = ObjectType.objects.get_or_create(
                    type=space_track_info['object_type']
                )
                obj_type.save()
                country_code, was_created = Country.objects.get_or_create(
                    code=space_track_info['country_code']
                )
                country_code.save()

                launch_parsed_date = iso_to_date_object(space_track_info['launch_date'])
                launch, was_created = Launch.objects.get_or_create(
                    launch_id=space_track_info['launch'],
                    date=launch_parsed_date,
                )
                launch.date = launch_parsed_date
                launch.save()

                space_track_parsed_date = iso_to_date_object(space_track_info['creation_date'])
                space_track, was_created = SpaceTrack.objects.get_or_create(
                    identifier=space_track_info['id'],
                    object_name=space_track_info['object_name'],
                    creation_date=space_track_parsed_date,
                    longitude=space_track_info['longitude'],
                    latitude=space_track_info['latitude'],
                    height_km=space_track_info['height_km'],
                    country_code=country_code,
                    object_type=obj_type,
                    launch=launch,
                )
                space_track.save()

            except Exception as e:
                printt(self, f'Error: {type(e)} {format(e)}')
                print(self, f'Error parsing launch date {space_track_info}')

        printt(self, 'End populating DB')
