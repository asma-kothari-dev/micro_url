# core python imports
import uuid
import urlparse
from random import randint

# django imports
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# project imports
import micro_url.settings as settings


alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$',
                              'Only alphanumeric characters are allowed.')


class MicroUrlQuerySet(models.query.QuerySet):
    """ QuerySet for MicroUrl model """

    def get_empty_query_set(self):
        """ Return empty queryset """

        return self.none()

    def get_micro_url_object(self, micro_url=None, alias=None):
        """ Filters queryset of MicroUrl model
        :return: queryset
        """

        if micro_url:
            # filtered queryset on the given micro url
            qs = self.filter(micro_url=micro_url)
        elif alias:
            # filtered queryset on the given alias
            qs = self.filter(alias=alias)
        else:
            # empty queryset
            qs = self.get_empty_query_set()

        return qs[0] if qs.count() > 0 else None

    def get_original_url(self, micro_url=None, alias=None):
        """ Original link of the micro url """

        micro_url_object = self.get_micro_url_object(
            micro_url=micro_url, alias=alias)
        return micro_url_object.link if micro_url_object else None


class MicroUrlManager(models.Manager):
    """ Manager of MicroUrl Model """

    pass


class MicroUrl(models.Model):
    """ Model for MicroUrl """

    link = models.URLField(unique=True, db_index=True,
                           help_text='A long url', verbose_name="URL*")
    alias = models.CharField(max_length=settings.SHORT_URL_MAX_LEN,
                             unique=True, db_index=True, blank=True, null=True,
                             help_text='A short code (Alphanumeric)',
                             verbose_name="Alias", validators=[alphanumeric])
    registered_at = models.DateTimeField(auto_now_add=True,
                                         help_text='Time at which the url is registered')
    submitter = models.ForeignKey(User,
                                  help_text='User who registerd the url')
    micro_url = models.URLField(max_length=settings.MICRO_URL_MAX_LEN,
                                unique=True, db_index=True, blank=True, null=True,
                                help_text='Shortened Url')
    objects = MicroUrlManager.from_queryset(MicroUrlQuerySet)()

    class Meta:
        db_table = 'shrink_microurl'

    def __str__(self):
        return self.alias

    def __get_random_user(self):
        """ Gets a random user from django-auth User model
        :return: :class: 'django.contrib.auth.models.User'
        """

        users = User.objects.all()
        x = randint(0, users.count() - 1)
        return users[x]

    def __set_submitter(self):
        """ Sets a random submitter for the short url request
        :return: None
        """

        self.submitter = self.__get_random_user()
        return

    def __get_random_code(self):
        """ Generates a random UUID
        :return: str
        """

        code = uuid.uuid4().hex
        return code[:settings.SHORT_URL_MAX_LEN]

    def __get_short_code(self):
        """ Gets you favourite alias or a random short code
        :return: str
        """

        if self.alias and \
                len(self.alias) >= settings.SHORT_URL_MAX_LEN:
            short_code = self.alias[:settings.SHORT_URL_MAX_LEN]
        else:
            short_code = self.__get_random_code()

        self.alias = short_code
        return short_code

    def __get_base_micro_url(self):
        """ BASE MICRO URL from settings
        :return: str
        """
        return settings.BASE_MICRO_URL

    def __set_micro_url(self):
        """ Micro Url developer
        :return: None """

        short_code = self.__get_short_code()  # get short code
        base_url = self.__get_base_micro_url()  # get base url
        self.micro_url = base_url + short_code  # develop micro url
        return

    def save(self, *args, **kwargs):
        """ Save the object after computing the micro url
        and associating it to a random submitter """

        self.__set_micro_url()
        self.__set_submitter()
        super(MicroUrl, self).save(*args, **kwargs)
        return
