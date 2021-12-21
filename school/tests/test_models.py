from django.test import TestCase
from school.models import ClassProfile, Subject


class TestModels(TestCase):
    def test_message_send(self):
        self.class_profile = ClassProfile.objects.create(
            name="bio-chem"
        )

        self.assertEquals(self.class_profile.name, "bio-chem")

    def test_class_profile_get_by_id(self):
        self.class_profile = ClassProfile.objects.create(
            name="bio-chem"
        )

        self.assertEquals(ClassProfile.get_by_id(self.class_profile.id), self.class_profile)

    def test_subject_remove(self):
        self.subject = Subject.objects.create(
            name="biologia"
        )

        self.assertEquals(Subject.remove(self.subject.id), True)
