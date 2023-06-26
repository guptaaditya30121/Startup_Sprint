from . models import Domain, Contest, User, Handle, Points, Time
import time
from datetime import datetime
import json
from urllib.request import urlopen
import requests
# import FileNotFoundError from django.core.exceptions


def UpdateData(get_response):

    def middleware(request):
        Mtime = Time.objects.first()
        if not Mtime:
            Mtime = Time(updater=0)
            Mtime.save()
        if time.time()-datetime.timestamp(Mtime.time) < 3*3600:
            response = get_response(request)
            return response
        else:
            Mtime.updater = 0
            Mtime.save()
            resp = requests.get(
                'https://codeforces.com/api/contest.list?gym=false').json()['result']

            for contest in resp:
                id = contest['id']
                url = f'https://codeforces.com/contestRegistration/{id}'
                db_contest = Contest.objects.filter(hostingSite=url).first()
                if db_contest and not db_contest.finished and contest['phase'] == 'FINISHED':
                    db_contest.finished = True
                    db_contest.save()
                    for user in User.objects.filter(contest_history__ref=db_contest.ref):
                        try:
                            handle = Handle.objects.filter(
                                user=user).first().handleName
                            response = json.load(urlopen(
                                f'https://codeforces.com/api/contest.standings?contestId={id}&handles={handle}'))['result']['rows'][0]['rank']
                            rank = Points(user=user, score=response,
                                          contest=db_contest)
                            rank.save()
                        except:
                            pass

                elif contest['phase'] == 'BEFORE':
                    domain = Domain.objects.filter(
                        name='https://codeforces.com/').first()
                    id = contest['id']
                    name = contest['name']
                    if (time.time() < contest['startTimeSeconds']) and not Contest.objects.filter(hostingSite=url).first():
                        upcoming_contest = Contest(hostingSite=url, timing=datetime.fromtimestamp(
                            contest['startTimeSeconds']), domain_contest=domain, name=name, ref=id)
                        upcoming_contest.save()
            response = get_response(request)
        return response
    return middleware
