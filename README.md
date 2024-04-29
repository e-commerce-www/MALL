# MALL


# 최신화를 위해 해야할 일들

# 내가 지금 작업중인 곳이 merge-branch-cy인지 확인 겸 이동.
# git checkout merge-branch-cy
# 확인 후 변경사항 모두 임시저장 
# git add .
# 변경했던 사항들 작성 + 로컬 저장소에 반영
# git commit -m "메세지내용"
# 작업한 내용물들 로컬 저장소(chanyeong)에 보관해두기 위해 브렌치 이동
# git checkout chanyeong
# 로컬 저장소(chanyeong)에 보관하기위해 merge 사용
# git merge merge-branch-cy
# 작업한 내용물이 저장 다 되었기에 main 브렌치 최신화 후 merge 밟아야함.
# main 브렌치로 이동
# git checkout main
# main 브렌치 최신화
# git pull
# 다른 사람이 작업한 db와 migrations 삭제
# python delete_migrations.py
# db.sqlite3 파일 삭제
# 작업용 브렌치로 이동
# git checkout merge-branch-cy
# 작업용 브렌치에 main 브렌치 변경내용 적용
# git merge main
# 작업용 브렌치에 main 브렌치 내용 적용 완료
# python manage.py migration
# python manage.py makemigrations
# python manage.py runserver
