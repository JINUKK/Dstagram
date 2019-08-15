from django import template

register = template.Library()

@register.filter
def follow_filter(index):
    user_list = []

    # for문에 있는 object를 대상으로 하는 것이기 때문에 follower를 씀
    for idx in index.follower.all():
        user_list.append(idx.me)

    return user_list

@register.filter
def follower_filter(index):
    user_list = []

    # for문에 있는 object를 대상으로 하는 것이기 때문에 follower를 씀
    for idx in index.following.all():
        user_list.append(idx.you)

    return user_list

