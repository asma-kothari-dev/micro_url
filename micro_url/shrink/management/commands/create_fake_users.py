import json

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from _random_users import RandomUserMixin


class Command(RandomUserMixin, BaseCommand):
    """ Commad to create fake users
    Usage:
        1. Create Users:
            python manage.py create_fake_users <count>
            :user_count: <type: 'int'> (Number of users to be created)
        2. Create and Display Users
            python manage.py create_fake_users <count> --display=True
    """

    help = 'Creates random users'

    def add_arguments(self, parser):
        """ Adds positional and optional (named) arguments.
        :return: None
        """

        # Positional arguments
        parser.add_argument('count', nargs='+', type=int)

        # Named (optional) arguments
        # Display Existing User
        parser.add_argument('--display',
                            action='store_true',
                            dest='display',
                            default=False,
                            help='Display existing users registered in the system')

    def handle(self, *args, **options):
        """ Handler creates random users with the given count.
        Uses API of randomuser.me to get random users. Registers them
        to django-auth User.
        """

        # Process Command Options
        # --------------------------------------------------------------

        # extract user count from the command options
        user_count = options.get('count', [])
        if not user_count:
            raise CommandError('User count should be provided.')
        try:
            user_count = int(user_count[0])
        except Exception:
            raise CommandError('User count should be an integer.')
        if user_count == 0:
            raise CommandError('User count should be greater than zero.')

        # extract display option from the command
        display = options.get('display')

        # get random users
        try:
            users = self._get_random_users(user_count)
        except Exception:
            raise CommandError('Failed to get random users')

        # register users
        try:
            for user in users:
                new_user = User(**user)
                new_user.save()
                if display:
                    self.stdout.write(str(user))
            # Successful registration of users
            self.stdout.write('\nSuccessfully created %d random user(s)'
                              % (user_count))
        except Exception:
            self.stdout.write('\nFailed to register random user(s)')
