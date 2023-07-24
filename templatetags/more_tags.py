from django import template

register = template.Library()

@register.filter(name='has_user_solved')
def has_user_solved(problem, user_obj):
    return problem.users.filter(id=user_obj.id).exists()