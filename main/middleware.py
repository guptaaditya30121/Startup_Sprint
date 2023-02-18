from . models import Domain, Contest, User, Handle, Points, Time
import time
from datetime import datetime
import json
from urllib.request import urlopen
# import FileNotFoundError from django.core.exceptions


def UpdateData(get_response):

    def middleware(request):
        Mtime = Time.objects.first()
        if  not Mtime:
            Mtime=Time(updater=0)
            Mtime.save()
        print(time.time(), datetime.timestamp(Mtime.time))
        if time.time()-datetime.timestamp(Mtime.time) < 1:
            response = get_response(request)
            return response
        else:
            print('middleware running')
            Mtime.updater = 0
            Mtime.save()
            resp = json.load(urlopen(
                'http://localhost:3000/result'))
            # ['result']

            for contest in resp:
                id = contest['id']
                url = f'https://codeforces.com/contestRegistration/{id}'
                db_contest = Contest.objects.filter(hostingSite=url).first()
                if db_contest and not db_contest.finished and contest['phase'] == 'FINISHED':
                    db_contest.finished = True
                    db_contest.save()
                    print('ipdate')
                    for user in User.objects.filter(contest_history__ref=db_contest.ref):
                        print('w')
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
                    # print(contest)
                    domain = Domain.objects.filter(
                        name='https://codeforces.com/').first()
                    id = contest['id']
                    name = contest['name']
                    if (time.time() < contest['startTimeSeconds']) and not Contest.objects.filter(hostingSite=url).first():
                        upcoming_contest = Contest(hostingSite=url, timing=datetime.fromtimestamp(
                            contest['startTimeSeconds']), domain_contest=domain, name=name, ref=id)
                        upcoming_contest.save()
                    print(contest)
            response = get_response(request)
        return response
    return middleware
