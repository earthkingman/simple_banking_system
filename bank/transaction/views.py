import json, bcrypt
from datetime import datetime, timedelta
from django.http  import JsonResponse
from django.views import View
# from django.db import transaction
from users.models import User
from account.models import Account
from transaction.models import Transaction

from django.core.paginator import Paginator ,EmptyPage, PageNotAnInteger
from transaction.tradeClass import Trade
from django.shortcuts import render, get_object_or_404
from users.utils      import login_decorator
# Create your views here.

class DepositView(View, Trade):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            deposit_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if super().check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIT_ERROR'},status=401)
                
            ex_account = super().check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=402)
                
            data = super().trade(ex_account, deposit_amount , description, t_type)
            if data == False : # 거래 가능 확인 및 거래 실시
                return JsonResponse({'Message':'BALANCE_ERROR'},status=403)

            return JsonResponse({'Message':'SUCCESS',"Data" : data}, status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=405) 
    
class WithdrawView(View, Trade):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            authenticated_user = request.user
            account_number = data['account_number']
            withdraw_amount = data['amount']
            description = data['description']
            t_type = data['t_type']
            
            if super().check_exit(authenticated_user, account_number) == False :# 계좌 존재 확인
                return JsonResponse({'Message':'EXIST_ERROR'},status=400)

            ex_account = super().check_auth(authenticated_user, account_number)
            if ex_account == False :# 계좌 권한 확인
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
            
            data = super().trade(ex_account, withdraw_amount , description, t_type)
            if data == False : # 거래 가능 확인 및 거래 실시
                return JsonResponse({'Message':'BALANCE_ERROR'},status=400)

            return JsonResponse({'Message':'SUCCESS',"Data" : data}, status=201)

        except KeyError:
            return JsonResponse({'Message':'ERROR'},status=400)


class ListView(View, Trade):
    @login_decorator ## 해당 계좌, 페이지
    def get(self, request):
        try:
            user = request.user
            account_number = request.GET.get("account_number", None)
            t_type = request.GET.get("t_type", None)
            date = request.GET.get("date", None)
            page = request.GET.get('page', 1)
 
             ## 해당계좌의 소유주가 맞는지 확인
            ex_account = Account.objects.get(account_number = account_number, user_id = user.id)
            if ex_account == None :
                return JsonResponse({'Message':'AUTH_ERROR'},status=400)
            
            results = self.get_transaction_list(ex_account, page, t_type, date)
        
            return JsonResponse({'Message':'SUCCESS', 'Data': results}, status=201)
        except KeyError:
            return JsonResponse({'Message':'ERROR'}, status=400)

    def get_transaction_list(self, ex_account, page, t_type, date):
        
             # Transaction 테이블의 해당 계좌 모든 거래내역을 불러온다.
            if t_type != None :
                transaction_list = Transaction.objects.filter(account_id = ex_account.id, t_type = t_type)
            elif date != None :
                transaction_list = Transaction.objects.filter(account_id = ex_account.id, created_at = date)
            else :
                transaction_list = Transaction.objects.filter(account_id = ex_account.id)
            #     
            # # Transaction 테이블의 모든 거래내역을 페이지네이터에서 10개씩 저장한다.
            try:
                paginator = Paginator(transaction_list, 10)
                page_obj = paginator.page(page) # page_obj = paginator.get_page(page)
                results = [{
                    '계좌 번호'   : ex_account.account_number,
                    '거래 후 잔액': page.balance,
                    '금액'      : page.amount,
                    '적요'      : page.description,
                    '거래 종류'  : page.t_type,
                    '거래 일시'  : page.created_at.strftime('%Y-%m-%d %H:%M:%S')
                    }for page in page_obj]
                return results

            except PageNotAnInteger:
                page_obj = paginator.page(1)
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)

         
            except KeyError:
                return False


 
class SeedView(View, Trade):
    def post(self, request):
        try :
            for i in range(1, 11):
                user = User.objects.create(
                    email        = "test" + str(i) + "@8Percent.com",
                    password     = bcrypt.hashpw("1234".encode('utf-8'),bcrypt.gensalt()).decode('utf-8')
                    )
                account = Account.objects.create(
                    user = user,
                    account_number = "계좌" + str(i),
                    balance = 1000
                )
                for j in range(1, 50000):
                    super().trade(account, 100 , "월급", "입금")
                    super().trade(account, 50 , "카드값", "출금")
            return JsonResponse({'Message':'SUCCESS'},status=200)

        except KeyError:
            return JsonResponse({'Message':'KEY_ERROR'},status=400)
