import datetime
from threading import Thread

from django.apps import AppConfig

from spaceXapi.settings import SPACECRAFT_FILE


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


@thread_task
def epoch_to_date_object(epoch):
    #  2020-10-13T02:56:59.566560
    date = datetime.datetime.fromtimestamp(epoch, tz=datetime.timezone.utc)
    return date


@thread_task
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
                pass

        return None


class ApiSpaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api_space'

    def ready(self):
        self.populate_db()
        print('api_space app is loaded', '*' * 50)

    @thread_task
    def populate_db(self):

        from api_space.models import Done
        done, _ = Done.objects.get_or_create()

        if done.file_mapped:
            print('File already mapped')
            return

        from api_space.models import SpaceTrack, ObjectType, Country, Launch
        from file_reader_tools.file_iterator import FileReader
        print('Start populating DB')

        file_reader = FileReader()
        file_content = file_reader.json_file_iterator(filename=SPACECRAFT_FILE)

        for space_track_info in file_content:

            space_track_info = flatten_data(space_track_info)

            obj_type, was_created = ObjectType.objects.get_or_create(
                type=space_track_info['object_type']
            )
            obj_type.save()
            country_code, was_created = Country.objects.get_or_create(
                code=space_track_info['country_code']
            )
            country_code.save()

            try:
                launch_parsed_date = iso_to_date_object(space_track_info['launch_date'])
                launch, was_created = Launch.objects.get_or_create(
                    launch_id=space_track_info['launch'],
                    date=launch_parsed_date,
                )
                launch.date = launch_parsed_date
                launch.save()
            except:
                print(f'Error parsing launch date {space_track_info["launch_date"]}')

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

        done.file_mapped = True
        done.save()
        print('End populating DB')
