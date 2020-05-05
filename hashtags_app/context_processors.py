from . import models
from django.core.cache import caches, cache

#todo one function for main and top 10
def top_ten_hash_tags(request):
    """if cache does not exists"""
    if not cache.get('top_ten_hash_tags'):
        """order hash tags by popularity"""
        hash_tags = models.HashTag.objects.order_by('-hit_count_generic__hits')

        top_ten = []

        for hash_tag in hash_tags:
            """if hash tags has any posts with it append it to the list"""
            if hash_tag.post_set.count() != 0:
                top_ten.append({"hash_tag": hash_tag,
                                "amount_oF_posts": hash_tag.post_set.count()})

            """once list has 10 hash_tags stop for loop"""
            if len(top_ten) == 9:
                break
        cache.set('top_ten_hash_tags', top_ten)
        return {"top_ten_hash_tags": top_ten}
    else:
        return {"top_ten_hash_tags": cache.get('top_ten_hash_tags')}