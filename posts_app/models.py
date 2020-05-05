from os.path import join
from uuid import uuid4

from hitcount.models import HitCount
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from hashtags_app.models import HashTag

lorem_ipsum = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce vestibulum risus purus, at maximus orci " \
              "scelerisque et. Sed lobortis rutrum ex nec cursus. Integer quam est, semper ut nibh at, bibendum tempus " \
              "magna. Quisque scelerisque ante et erat ornare varius. Vivamus ut nisi vulputate, laoreet magna quis, " \
              "fringilla enim. Donec leo est, vestibulum vitae scelerisque vel, tristique eget lacus. Sed pellentesque " \
              "elementum tortor, vulputate suscipit velit fermentum ut. Curabitur blandit cursus dolor, in sodales quam " \
              "tincidunt sit amet. In vitae odio in mi tincidunt mattis. Donec semper libero ligula, et bibendum nisl " \
              "imperdiet sed. Proin commodo est turpis, vel volutpat magna congue eleifend. In maximus ex sed purus " \
              "semper, et sagittis ex lobortis. Nulla vitae scelerisque risus. Aenean sed mollis dui. Proin ut libero " \
              "porttitor, cursus est sit amet, feugiat metus. Nunc semper arcu vel viverra aliquam. Pellentesque at " \
              "magna ipsum. Proin nec viverra sem. Morbi interdum, augue non ultricies sodales, diam massa ultricies " \
              "libero, vitae ultricies augue orci quis lectus. Vivamus dictum arcu non malesuada vehicula. In non " \
              "tincidunt nulla, nec rutrum est. Cras eleifend ultrices nisl, sed vulputate nibh bibendum vel. Aliquam " \
              "et purus rutrum, tempus ligula sit amet, tincidunt nibh. Nulla vel volutpat odio, et consectetur nibh." \
              " Vestibulum mattis magna et lobortis consectetur. Donec eget arcu aliquet, dictum metus non, rhoncus " \
              "magna. Maecenas rhoncus auctor pulvinar. Praesent sit amet metus erat. Nunc eget est id lacus finibus " \
              "tempus a non nulla. Ut fringilla, urna vel lacinia imperdiet, dui tortor ultricies ligula, et aliquam" \
              "eros odio sed lacus. Vestibulum id varius justo, vitae pretium leo. Integer vel convallis metus. Fusce " \
              "dapibus dui vel risus suscipit, sed ultricies ligula fermentum. Morbi quis convallis nunc. Donec placerat" \
              " nisi metus, ac imperdiet felis commodo in. Suspendisse in mauris augue. Ut vestibulum cursus quam, sit" \
              " amet condimentum dolor. Suspendisse elementum semper pellentesque. Duis accumsan ante metus, et volutpat" \
              " mauris tincidunt vitae. Sed dapibus commodo felis a finibus. Sed eget tortor sit amet neque dapibus " \
              "imperdiet. Donec porta elementum massa, sed euismod tellus hendrerit eget. Pellentesque sagittis " \
              "sollicitudin massa sit amet feugiat. Donec sed molestie mi. Etiam ultricies scelerisque nulla id tempus. " \
              "Vestibulum eu dui at libero scelerisque tempor scelerisque ut mauris. Integer posuere, justo eu " \
              "sollicitudin laoreet, nulla nunc mollis neque, vitae dapibus nisl ipsum a orci. Fusce commodo lectus " \
              "augue, ac viverra dolor bibendum in. In dignissim varius dolor, a ornare nulla aliquam in. Mauris " \
              "finibus elit ac metus aliquet sodales. In consequat eget nibh sit amet mattis. Curabitur et gravida " \
              "lectus, commodo hendrerit nisl. Donec massa diam, sodales at ultrices sit amet, mollis a urna. " \
              "Phasellus vel massa sem. Praesent vulputate erat ac consectetur placerat. Aliquam erat volutpat. " \
              "Quisque quis odio id velit semper viverra et quis nibh. Curabitur semper elit a leo vulputate molestie. " \
              "Vestibulum lobortis purus id finibus aliquam. Suspendisse orci sem, consectetur nec ligula vel, finibus " \
              "egestas augue."


def update_filename(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "{}.{}".format(uuid4(), ext)
    return new_filename


# Create your models here.
class Post(models.Model):
    date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField(null=False, default=lorem_ipsum)
    hash_tags = models.ManyToManyField(HashTag, blank=True)
    title = models.CharField(max_length=124, default="Test Title")
    picture = models.ImageField(upload_to=update_filename, default=None, blank=True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
                                        related_query_name='hit_count_generic_relation')

    """ 
        For development only 
        overrided save function, it saves twice once to create object and then again to get object id and save 
        picture papath after uploading picture
    """
    if settings.DEBUG:
        def save(self, *args, **kwargs):
            super(Post, self).save(*args, **kwargs)
            if self.title == "Test Title":
                self.title += " {}".format(self.id)
            super(Post, self).save(*args, **kwargs)

    def get_picture_path(self):
        return join("https://", settings.AWS_S3_CUSTOM_DOMAIN, settings.AWS_LOCATION, self.picture.__str__())

    def __str__(self):
        return self.title