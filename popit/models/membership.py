from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from popit.models.exception import PopItFieldNotExist
from popit.models import Person
from popit.models import Organization
from popit.models import Post
from popit.models import Link
from popit.models import ContactDetail
from popit.models import Area
import uuid


class Membership(TranslatableModel):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    translated = TranslatedFields(
        label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Label")),
        role = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("role")),

    )

    person = models.ForeignKey(Person, verbose_name=_("person"), related_name="memberships")
    # Used with organization for now. I think this going to break the spec
    member = models.ForeignKey(Organization, null=True, blank=True, verbose_name=_("member"), related_name="member")
    organization = models.ForeignKey(Organization, null=True, blank=True, verbose_name=_("organization"), related_name="memberships")
    post = models.ForeignKey(Post, null=True, blank=True, verbose_name=_("post"), related_name="memberships")
    on_behalf_of = models.ForeignKey(Organization, null=True, blank=True, verbose_name=_("on_behalf_of"), related_name="on_behalf_of")
    area = models.ForeignKey(Area, null=True, blank=True, verbose_name=_("area"))
    start_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("start date"),
                                  validators=[
                                      RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                  ]
        )
    end_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("end date"),
                                validators=[
                                      RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                  ]
                                )
    contact_details = GenericRelation(ContactDetail)
    links = GenericRelation(Link)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def citation_exist(self, field):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        links = self.links.language(self.language_code).filter(field=field)
        if links:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.id:
            id_ = uuid.uuid4()
            self.id = str(id_.hex)

        self.full_clean()

        super(Membership, self).save(*args, **kwargs)

    def clean(self):
        # This never get called, but we override save anyway for the uuid thingy
        if not self.post and not self.organization:
            raise ValidationError("A person must be a member of a post or organization")

        if self.post and self.organization:
            post_org = self.post.organization
            if post_org:
                if post_org != self.organization:
                    raise ValidationError("An organization for membership should match organization of a post")

        super(Membership, self).clean()

    def __unicode__(self):
        # Why is it that they do not find name, but need self.name
        # Actually what could go wrong if we switch to bm
        if not self.label:
            if self.post:
                return "%s of %s" % (self.person.safe_translation_getter("name", self.person.id), self.post.safe_translation_getter("role", self.post.id))
            elif self.organization:
                return "%s member of %s" % (self.person.safe_translation_getter("name", self.person.id),
                                            self.organization.safe_translation_getter("name", self.organization.id))
        return self.safe_translation_getter('label', self.id)
