from django.core.management.base import BaseCommand
from django.db import IntegrityError
from cms_api.models import *
import json


""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


# clear or delete previous data
def clear_data():
    AppUser.objects.filter(email='admin@admin.com').delete()
    Country.objects.all().delete()
    State.objects.all().delete()
    City.objects.all().delete()

    print("Deleted previous data !!!")

# create country,state,city data
def create_address():
    try:
        with open('city.json') as f:
            data = json.load(f)
            print("data loaded")
    except:
        print('unable to load file !! please check again')

    print("inserting data")

    # create country
    country = Country()
    country.name = 'India'
    country.save()

    print("country created !!")

    for obj in data:
        # create state and save data
        try:
            state = State()
            state.name = obj['state']
            state.country_instance = country
            state.save()
            print("country created !!", state.name)
        except:
            pass

    # get all state
    all_state = State.objects.all()

    # create city under state
    for state in all_state:
        for obj in data:
            if state.name == obj['state']:
                city = City()
                city.name = obj['city']
                city.state_instance = state
                city.save()
                print("city created !!", city.name)

    status = 200
    return status

# create admin user
def create_admin():
    try:
        admin_user = AppUser()
        admin_user.email = 'admin@admin.com'
        admin_user.username = 'admin@admin.com'
        admin_user.phone = 8408838888
        admin_user.pincode = 413808
        admin_user.set_password('admin123')
        admin_user.is_superuser = 1
        admin_user.save()
        # message
        print("super user created!!")
    except IntegrityError:
        print("unable to create superuser !! please try again")


def run_seed(self, mode):
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    # create admin user
    create_admin()

    # creating addresses
    create_address()
