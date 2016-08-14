from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.conf import settings

import utils
from scraper_monitor.models import Scraper


@user_passes_test(lambda u: u.is_superuser)
def monitor_scraper(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Method Not Allowed")
    items_number, images_number = utils.get_mongo_stats()
    mongo_url = settings.MONGO_URI
    mongo_db = settings.MONGO_DATABASE
    mongo_col = settings.MONGO_POSTCARDS_COLLECTION
    scrapers = []
    for s in Scraper.objects.all():
        checking_url = s.ws_url + '/listjobs.json'
        stats = utils.verify_spider(s.spider_name, checking_url, s.scraper_project_name)
        s_dict = {}
        s_dict['obj'] = s
        s_dict.update(stats)
        scrapers.append(s_dict)
        if stats.has_key('job_id'):
            s.job_id = stats['job_id']
            s.save()

    context = {
        'scrapers': scrapers,
        'items_number': items_number,
        'images_number': images_number,
        'mongo_url': mongo_url,
        'mongo_db': mongo_db,
        'mongo_col': mongo_col
    }
    return render(request, 'homepage.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def start_spider(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Method Not Allowed")

    scraper_id = request.GET.get('id')
    try:
        scraper = Scraper.objects.get(pk=scraper_id)
        url = scraper.ws_url + '/schedule.json'
        res = utils.start_spider(scraper.spider_name, url, scraper.scraper_project_name)
        if res:
            messages.info(request, 'Start scraper %s successfully' % scraper.name, fail_silently=True)
            scraper.job_id = res
            scraper.save()
        else:
            messages.error(request, "Can not start scraper %s" % scraper.name)
    except:
        messages.error(request, "Can not find the scraper with id %s" % id, fail_silently=True)
        pass

    return redirect('/')


@user_passes_test(lambda u: u.is_superuser)
def stop_spider(request):
    if request.method != 'GET':
        return HttpResponseBadRequest("Method Not Allowed")

    scraper_id = request.GET.get('id')
    try:
        scraper = Scraper.objects.get(pk=scraper_id)
        url = scraper.ws_url + '/cancel.json'
        res = utils.stop_spider(scraper.scraper_project_name, url, scraper.job_id)
        if res:
            messages.info(request, 'Stop scraper %s successfully' % scraper.name, fail_silently=True)
        else:
            messages.error(request, "Can not stop scraper %s" % scraper.name)
    except:
        messages.error(request, "Can not find the scraper with id %s" % id, fail_silently=True)
        pass

    return redirect('/')