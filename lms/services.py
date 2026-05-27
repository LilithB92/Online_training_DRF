from lms.models import CourseSubscription


def get_course_subscribed_user(course_id):
    """Получает ID курса и возвращает почты пользователей подписанных к этому курсу."""

    course_subscrabtions = CourseSubscription.objects.filter(course=course_id)
    return [course_subscrabtion.user.email for course_subscrabtion in course_subscrabtions if course_subscrabtions]
