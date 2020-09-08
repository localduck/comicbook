from django import template

register = template.Library()


@register.simple_tag
def blaze(auth, comic_info, user):
    black_list = ['ad', 'ht']
    if auth:
        first_list = ['dk', 'dc', 'mr', 'ad', 'ht', 'at']
        second_list = [user.darck_comic, user.dc_comic, user.marvel_comic, user.adult_comic, user.hentai_comic, 1]
        choice_list = [i[0] for i in zip(first_list, second_list) if i[1]]
        if (comic_info not in choice_list and comic_info in first_list) or\
                (user.age < 18 if comic_info in black_list else False):
            return 'blazed'
    else:
        if comic_info in black_list:
            return 'blazed'
    return ''
