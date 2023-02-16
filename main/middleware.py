import requests
from . models import Domain, Contest, User, Handle, Points
import time
from datetime import datetime


async def upcoming():
    response = requests.get(
        'https://codeforces.com/api/contest.list').json()['result']
    domain = Domain.objects.filter(name='https://codeforces.com/').first()
    for contest in response:
        url = f'https://codeforces.com/contestRegistration/{id}'
        db_contest = Contest.object.filter(hostingSite=url).first()
        if db_contest and contest['phase'] == 'FINISHED':
            db_contest.finished = True
            db_contest.save()
            for user in User.objects.filter(contest_history__id=db_contest.id):
                handle = Handle.objects.filter(user=user).first().handleName
                response = requests.get(
                    f' https://codeforces.com/api/contest.standings?contestId={id}?handles={handle}').json()['results']['rows'][0]['rank']
                rank = Points(user=user, score=response, contest=db_contest)
                rank.save()

        elif contest['phase'] == 'BEFORE':
            id = contest['id']
            if time.time() < contest['startTimeSeconds'] and not Contest.object.filter(hostingSite=url).first():
                upcoming_contest = Contest(hostingSite=url, timing=datetime.fromtimestamp(
                    contest['startTimeSeconds']), domain_contest=domain)
                upcoming_contest.save()
