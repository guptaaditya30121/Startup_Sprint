import requests
from . models import Domain, Contest, User, Handle, Points
import time
from datetime import datetime


def UpdateData(get_response):

    def middleware(request):
        print('contest')
        resp = requests.get(
            'https://codeforces.com/api/contest.list?gym=false').json()['result']
        domain = Domain.objects.filter(name='https://codeforces.com/').first()
        for contest in resp:
            id = contest['id']
            url = f'https://codeforces.com/contestRegistration/{id}'
            db_contest = Contest.objects.filter(hostingSite=url).first()
            if db_contest and contest['phase'] == 'FINISHED':
                db_contest.finished = True
                db_contest.save()
                for user in User.objects.filter(contest_history__id=db_contest.id):
                    handle = Handle.objects.filter(
                        user=user).first().handleName
                    response = requests.get(
                        f' https://codeforces.com/api/contest.standings?contestId={id}?handles={handle}').json()['results']['rows'][0]['rank']
                    rank = Points(user=user, score=response,
                                  contest=db_contest)
                    rank.save()

            elif contest['phase'] == 'BEFORE':
                print(contest)
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
