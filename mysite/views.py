import datetime
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data, get_yesterday_hot_data


def get_seven_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date) \
                        .values('id', 'title') \
                        .annotate(read_num_sum=Sum('read_details__read_num')) \
                        .order_by('-read_num_sum')
    return blogs[:7]

def home(request):
    blog_contennt_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_contennt_type)
    today_hot_data = get_today_hot_data(blog_contennt_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_contennt_type)

    # 获取7天热门博客的缓存数据
    seven_days_hot_blog = cache.get('seven_days_hot_blog')
    if seven_days_hot_blog is None:
        seven_days_hot_blog = get_seven_days_hot_blogs()
        cache.set('seven_days_hot_blog', seven_days_hot_blog, 600)
    #     print('calc')
    # else:
    #     print('use chche')

    context = { 
        'dates': dates,
        'read_nums': read_nums,
        'today_hot_data': today_hot_data,
        'yesterday_hot_data': yesterday_hot_data,
        'seven_days_hot_blog': seven_days_hot_blog,
    }
    return render(request, 'home.html', context)


# 消息中心
def my_notifications(request):
    context = {}
    return render(request, 'my_notifications.html', context)
