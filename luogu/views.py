import time
import json
import random
from .models import Customer, Commodity, Staff, Order, Order_detail, Shipping_address, Shopping_cart_details, Sales
import markdown
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import User
from django.contrib import auth
from fuzzywuzzy import fuzz
# from .myforms import CreateArticleForm, CreateQuestion
import datetime
# from extra_apps.xadmin.views import CommAdminView
from xadmin.views import CommAdminView

# Create your views here.

# dev = True
dev = False


def index(request):
    if request.method == "POST":
        print(request.POST.get('submit'))
        if request.POST.get('submit') == "logout":
            auth.logout(request)
        return redirect('/')
    else:
        try:
            login = True if request.user.is_authenticated else False
            print(login)
            username = None
            if login:
                try:
                    username = Customer.objects.get(user=request.user).user_name
                except:
                    try:
                        username = Staff.objects.get(user=request.user).user_name
                    except:
                        pass
            print(username)
            products = Commodity.objects.all()
            print(products)

            hot = []
            products_num = len(products)
            if products_num == 0:
                pass
            else:
                for i in range(4):
                    now = i % products_num
                    hot.append({
                        "commodity_id": products[now].id,
                        "name": products[now].name,
                        "purchase_price": products[now].purchase_price,
                        "selling_price": products[now].selling_price,
                        "img": products[now].img,
                        "left": (i+1)*243
                    })

            renqi = []
            for i in range(5):
                now = i % products_num
                renqi.append({
                    "commodity_id": products[now].id,
                    "name": products[now].name,
                    "purchase_price": products[now].purchase_price,
                    "selling_price": products[now].selling_price,
                    "img": products[now].img,
                    "left": (i)*243
                })

            newProduct = []
            for i in range(5):
                now = i % products_num
                newProduct.append({
                    "commodity_id": products[now].id,
                    "name": products[now].name,
                    "purchase_price": products[now].purchase_price,
                    "selling_price": products[now].selling_price,
                    "img": products[now].img,
                    "left": (i) * 243
                })

            series = []
            top = 76
            left = 25
            for i in range(9):
                now = i % products_num
                series.append({
                    "commodity_id": products[now].id,
                    "name": products[now].name,
                    "selling_price": products[now].selling_price,
                    "img": products[now].img,
                    "detail": products[now].detail,
                    "left": left,
                    "top": top
                })
                left += 313
                if left > 800:
                    left = 25
                    top += 117

            ret = {"hots": hot, "login": login, "username": username,
                   "renqi": renqi, "newProduct": newProduct, "series": series}
            return render(request, "index.html", ret)
        except:
            return render(request, "index.html")
    # return render(request, "index.html")


# gouwuche
@login_required
def shopping_cart(request):
    if request.method == "POST":
        print(request.POST)
        # list = request.POST.getlist("check_box_list")
        user = request.user
        try:
            customer = Customer.objects.get(user=user)
        except:
            customer = Staff.objects.get(user=user)
        buy = request.POST.getlist("buy[]")
        num = request.POST.getlist("num[]")
        if len(buy) == 0:
            return JsonResponse({"result": False, "message": "请选择商品"})
            # return HttpResponse("妈的搞你妈呢")  # 最后返会给前端的数据，如果能在前端弹出框中显示我们就成功了
        products = []
        total_amount = 0
        for i in range(len(buy)):
            if int(num[i]) > Commodity.objects.get(id=int(buy[i])).stock:
                return JsonResponse({"result": False, "message": "库存不足"})
            products.append({
                "commodity_id": int(buy[i]),
                "num": num[i]
            })
        print(products)
        staff = Staff.objects.all()[0]
        order = Order(staff=staff, customer=customer)
        order.save()
        for product in products:
            product_id = product["commodity_id"]
            num = int(product["num"])
            commodity = Commodity.objects.get(id=product_id)
            order_detail = Order_detail(order=order, commodity=commodity, quantity=num)
            order_detail.save()
            total_amount += commodity.selling_price * num

            # 清空购物车
            shopping_cart_detail = Shopping_cart_details.objects.filter(commodity=commodity, customer=customer)[0]
            shopping_cart_detail.quantity = 0
            shopping_cart_detail.save()

        # order.total_amount = total_amount
        # order.real_payment = total_amount
        order.save()
        customer.consumption_amount += order.total_amount
        customer.save()
        return JsonResponse({"result": True, "order_id": order.id})
        # return redirect("/订单结算.html/" + str(order.id))
    else:
        login = True if request.user.is_authenticated else False
        print(login)
        username = None
        if login:
            username = Customer.objects.get(user=request.user).user_name
        user = request.user
        print(user)
        customer = Customer.objects.get(user=user)
        shopping_cart = Shopping_cart_details.objects.filter(customer=customer)
        ls = []
        num = 0
        for product in shopping_cart:
            if product.quantity:
                ls.append({
                    "img": product.commodity.img,
                    "name": product.commodity.name,
                    "standard": product.commodity.standard,
                    "selling_price": product.commodity.selling_price,
                    "quantity": product.quantity,
                    "commodity_id": product.commodity.id,
                    "top": num * 140
                })
                num += 1

        same_products = Commodity.objects.all()
        nums = len(same_products)
        ret_same_products = []
        left = 0
        for i in range(5):
            ret_same_products.append({
                "id": same_products[i % nums].id,
                "img": same_products[i % nums].img,
                "name": same_products[i % nums].name,
                "selling_price": same_products[i % nums].selling_price,
                "left": left,
            })
            left += 210

        ret = {
            "products": ls, "login": True, "username": customer.user_name,
            "down_top1": 140 * num + 236,
            "down_top2": 140 * num + 338,
            "down_top3": 140 * num + 338 + 399,
            "login": login, "username": username,
            "ret_same_products": ret_same_products
        }
        return render(request, "购物车.html", ret)


@login_required
def shopping_cart_change(request):
    if request.method == "POST":
        try:
            user = request.user
            customer = Customer.objects.get(user=user)
            if request.POST.get("operate") == "delete":
                id = request.POST.get("id")
                commodity = Commodity.objects.get(id=id)
                try:
                    shopping_cart_details = Shopping_cart_details.objects.filter(commodity=commodity, customer=customer)[0]
                    shopping_cart_details.quantity = 0
                    shopping_cart_details.save()
                except:
                    pass
                return JsonResponse({"res": True})
            elif request.POST.get("operate") == "change":
                id = request.POST.get("id")
                num = request.POST.get("num")
                commodity = Commodity.objects.get(id=id)
                detail = Shopping_cart_details.objects.filter(commodity=commodity, customer=customer)[0]
                detail.quantity = num
                detail.save()
                print(id)
                print(num)
        except:
            pass
        return JsonResponse({"res": True})


@login_required
def personal_center(request):
    return render(request, "个人中心.html")


# dingdanjiesuan
@login_required
def order_settlement(request, order_id):
    order = Order.objects.get(id=order_id)
    customer = order.customer
    if request.method == "POST":

        pass
    else:
        login = True if request.user.is_authenticated else False
        print(login)
        username = None
        if login:
            username = Customer.objects.get(user=request.user).user_name
        print("order_settlement1")
        order_details = Order_detail.objects.filter(order=order)
        print("order_settlement2")
        details = []
        num = 0
        for detail in order_details:
            commodity = detail.commodity
            # commodity = Commodity.objects.get(id=detail.commodity_id)
            details.append({
                "img": commodity.img,
                "name": commodity.name,
                "detail": commodity.detail,
                "unit_price": commodity.selling_price,
                "num": detail.quantity,
                "sum": detail.quantity * commodity.selling_price,
                "real_payment": detail.quantity * commodity.selling_price,
                "top1": 500 + 120 * num,
                "top2": 520 + 120 * num,
                "top3": 525 + 120 * num,
                "top4": 560 + 120 * num,
                "top5": 510 + 120 * num
            })
            num += 1
            # break
        print("order_settlement3")
        addresses = []
        default_address = {
            "name": "梁泽荣",
            "telephone": "13691637045",
            "address": "广东省深圳市南山区粤海街道深圳大学3688号",
            "address_tag": "我",
        }
        address_num = 0
        for address in Shipping_address.objects.filter(customer=customer):
            addresses.append({
                "address_id": address_num,
                "name": address.name,
                "telephone": address.telephone,
                "address": address.area + address.address,
                "address_tag": address.address_tag,
                "top": address_num * 183 + 80
            })

            address_num += 1
            if address_num == 1:
                default_address = addresses[0]
            elif address_num == 3:
                break
        ret = {
            "details": details, "detail_height": 70 + 120 * num, "invoice_top": 500 + 120 * num,
            "down_top": 1060 + 120 * num,
            "login": True, "order_id": order_id,
            "order": order, "addresses": addresses,
            "default_address": default_address,
            "login": login, "username": username,
        }
        return render(request, "订单结算.html", ret)


@login_required
def order_details(request, order_id):
    login = True if request.user.is_authenticated else False
    print(login)
    username = None
    if login:
        username = Customer.objects.get(user=request.user).user_name
    order = Order.objects.get(id=order_id)
    details = {
        "order_id": order.id,
        "payment_status": "已付款" if order.payment_status else "未付款",
        "name": order.name,
        "address": order.area + order.address,
        "telephone": order.telephone,
        "payment_method": order.payment_method,
        "total_amount": order.total_amount,
        "real_payment": order.real_payment,
        "shipping": order.shipping,

        # "order_id": order.id,
        # "payment_status": "已付款",
        # "name": "梁泽荣",
        # "address": "深圳大学",
        # "telephone": "123123123",
        # "payment_method": "在线支付",
        # "total_amount": 666,
        # "real_payment": 777,
        # "shipping": 50,
    }
    # print(details)
    products = []
    order_details = Order_detail.objects.filter(order=order)
    num = 0
    for order_detail in order_details:
        commodity = order_detail.commodity
        # commodity = Commodity.objects.get(id=order_detail.commodity_id)
        products.append({
            "img": commodity.img,
            "name": commodity.name,
            "detail": commodity.detail,
            "unit_price": commodity.selling_price,
            "num": order_detail.quantity,
            "sum": order_detail.quantity * commodity.selling_price,
            "real_payment": order_detail.quantity * commodity.selling_price,
            "standard": commodity.standard,
            "top": 120 * num - 1,
        })
        num += 1
    heights = {
        "height1": 1070 + 120 * num - 1,
        "height2": 1113 + 120 * num - 1,
        "height3": 1155 + 120 * num - 1,
        "height4": 1197 + 120 * num - 1,
    }
    ret = {
        "details": details, "down_height": 210 + 120 * num, "login": True,
        "products": products, "heights": heights, "down_down_height": 1315 + 120 * num,
        "pay_button": True if details["payment_status"] == "未付款" else False,
        "login": login, "username": username,
    }
    print(ret)
    return render(request, "订单详情.html", ret)


@login_required
def order_management(request):
    login = True
    username = None
    if login:
        try:
            username = Customer.objects.get(user=request.user).user_name
        except:
            pass
    user = request.user
    print(user)
    customer = Customer.objects.get(user=user)
    print(customer)
    orders = []
    ls = Order.objects.filter(customer=customer).order_by('-id')
    num = 0
    for order in ls:
        try:
            one_of_order_detail = Order_detail.objects.filter(order=order)[0]
            product = one_of_order_detail.commodity
            # product = Commodity.objects.get(id=one_of_order_detail.commodity_id)

            orders.append({
                "order_id": order.id,
                "time": order.order_creation_time,
                "total_amount": order.total_amount,
                "shipping": order.shipping,
                "img": product.img,
                "name": product.name,
                "standard": product.standard,
                "num": one_of_order_detail.quantity,
                "height": 185 * num
            })
            num += 1
        except:
            pass
    return render(request, "订单管理.html", {"login": login, "username": username,
                                         "orders": orders, "downtop": max(1000, 435 + num * 185)})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not username or not password:
            return JsonResponse({"result": False, "message": "傻逼"})
        try:
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                request.session['is_login'] = True
                request.session['user_id'] = str(user.id)
                request.session['user_name'] = str(user)

                return HttpResponseRedirect('/')
            else:
                message = "密码不正确!"
        except:
            message = "用户不存在!"
        return JsonResponse({"result": False, "message": message},json_dumps_params={'ensure_ascii':False})
    else:
        return render(request, "用户登录.html")


def user_register(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            password = request.POST.get("password")
            user = User(username=name)
            user.set_password(password)
            user.save()
            customer = Customer(user=user, user_name=name)
            customer.save()
            return JsonResponse({"result": True})
        except:
            return JsonResponse({"result": False})

    else:
        return render(request, "用户注册.html")


@login_required
def address_management(request):
    return render(request, "地址管理.html")


def product_details(request, product_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("/用户登录.html")
        num = int(request.POST.get('num'))
        print(num)
        operate = request.POST.get('submit')
        user = request.user
        customer = Customer.objects.get(user=user)
        commodity = Commodity.objects.get(id=product_id)
        if num > commodity.stock:
            return redirect("/商品详情页.html/" + str(product_id))
        staff = Staff.objects.all()[0]
        if operate == "buy":
            print("buy")
            order = Order(staff=staff, customer=customer)
            print(order.id)
            order.save()
            print(order.id)
            order_detail = Order_detail(order=order, commodity=commodity, quantity=num)
            print(order_detail.id)
            order_detail.save()
            customer.consumption_amount += order.total_amount
            customer.save()
            print(order_detail.id)
            return redirect("/订单结算.html/" + str(order.id))
            # return redirect("/")
        elif operate == "add":
            print("add")
            try:
                shopping_cart_details = Shopping_cart_details.objects.get(commodity=commodity, customer=customer)
            except:
                shopping_cart_details = Shopping_cart_details(commodity=commodity, customer=customer,
                                                              unit_price=commodity.selling_price, quantity=0)
            print("add1")
            shopping_cart_details.quantity += num
            print("add2")
            shopping_cart_details.save()
            return redirect("/商品详情页.html/" + str(product_id))
    else:
        try:
            login = True if request.user.is_authenticated else False
            print(login)
            username = None
            if login:
                username = Customer.objects.get(user=request.user).user_name
            product = Commodity.objects.get(id=product_id)
            details = {
                "img": product.img,
                "name": product.name,
                "purchase_price": product.purchase_price,
                "selling_price": product.selling_price,
                "sales": product.sales,
                "origin_address": product.origin_address,
                "production_date": product.production_date,
                "shelf_life": product.shelf_life,
                "standard": product.standard,
                "detail": product.detail,
                "stock": product.stock
            }
            same_products = Commodity.objects.all()
            nums = len(same_products)
            ret_same_products = []
            left = 0
            top = 1218
            for i in range(5):
                ret_same_products.append({
                    "id": same_products[i%nums].id,
                    "img": same_products[i%nums].img,
                    "name": same_products[i%nums].name,
                    "selling_price": same_products[i%nums].selling_price,
                    "left": left,
                    "top": top
                })
                left += 215
                top += 296
            ret = {
                "details": details,
                "login": login,
                "username": username,
                "same_products": ret_same_products
            }
            return render(request, "商品详情页.html", ret)
        except:
            return render(request, "商品下架.html")
    # return render(request, "商品详情页.html")


def product_classification(request):
    login = True if request.user.is_authenticated else False
    print(login)
    username = None
    if login:
        username = Customer.objects.get(user=request.user).user_name
    products = Commodity.objects.all()
    ret = []
    left = 0
    top = 485
    for product in products:
        ret.append({
            "commodity_id": product.id,
            "name": product.name,
            "purchase_price": product.purchase_price,
            "selling_price": product.selling_price,
            "img": product.img,
            "left": left,
            "top": top
        })
        left += 243
        if left > 1000:
            left = 0
            top += 295

    return render(request, "商品分类.html", {"products": ret, "login": login, "username": username,})


def popular_recommendation(request):
    return render(request, "人气推荐.html")


@login_required
def payment_method_selection(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == "POST":
        name = request.POST.get("name")
        telephone = request.POST.get("telephone")
        address = request.POST.get("address")
        print(name)
        print(telephone)
        print(address)
        order.name = name
        order.telephone = telephone
        order.address = address
        order.save()
        return HttpResponse({"good": 1})
    else:
        login = True if request.user.is_authenticated else False
        print(login)
        username = None
        if login:
            username = Customer.objects.get(user=request.user).user_name
        return render(request, "选择支付方式.html", {"order_id": order_id, "payment": order.real_payment, "login": login, "username": username,})


@login_required
def third_party_payment(request, order_id):
    if request.method == "POST":
        return redirect("/支付成功.html/" + str(order_id))
        pass
    else:
        real_payment = Order.objects.get(id=order_id).real_payment
        return render(request, "第三方支付.html", {"order_id": order_id, "real_payment": real_payment})


@login_required
def successful_payment(request, order_id):
    login = True if request.user.is_authenticated else False
    print(login)
    username = None
    if login:
        username = Customer.objects.get(user=request.user).user_name
    order = Order.objects.get(id=order_id)
    order.payment_status = True
    order.save()
    order_details = Order_detail.objects.filter(order=order)
    for order_detail in order_details:
        commodity = order_detail.commodity
        # commodity = Commodity.objects.get(id=order_detail.commodity_id)
        commodity.stock -= order_detail.quantity
        commodity.sales += order_detail.quantity
        commodity.save()
    details = {
        "order_creation_time": order.order_creation_time,
        "total_amount": order.total_amount,
        # "total_amount": 666,
        "shipping": order.shipping,
        # "shipping": 50,
        "real_payment": order.real_payment,
        # "real_payment": 777,
        # "order_creation_time": order.order_creation_time,
        "name": order.name,
        # "name": "梁泽荣",
        "telephone": order.telephone,
        # "telephone": 123123123,
        "address": order.area + order.address
        # "address": "深圳大学"
    }

    same_products = Commodity.objects.all()
    nums = len(same_products)
    ret_same_products = []
    left = 0
    for i in range(5):
        ret_same_products.append({
            "id": same_products[i % nums].id,
            "img": same_products[i % nums].img,
            "name": same_products[i % nums].name,
            "selling_price": same_products[i % nums].selling_price,
            "left": left,
        })
        left += 233

    ret = {
        "details": details,
        "order_id": order_id,
        "login": login,
        "username": username,
        "ret_same_products": ret_same_products
    }
    return render(request, '支付成功.html', ret)


def similar_products(request):
    return render(request, "相似商品.html")


def user_privacy_agreement(request):
    return render(request, "用户隐私协议.html")


@login_required
def collection(request):

    return render(request, "我的收藏.html")


def interested_classification(request):
    return render(request, "感兴趣都分类.html")


def online_service(request):
    return render(request, "在线客服.html")


def help_center(request):
    return render(request, "购物常见问题.html")



from django.http import HttpResponse
from django.shortcuts import render_to_response
import json

@login_required
def get_address(request, id):
    print(">>>")
    user = request.user
    customer = Customer.objects.get(user=user)
    address = Shipping_address.objects.filter(customer=customer)[id]
    rlist = [{"name": address.name,
               "telephone": address.telephone,
               "address": address.address}]
    rjson = json.dumps(rlist)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response


@login_required
def new_address(request):
    if request.method == "POST":
        user = request.user
        customer = Customer.objects.get(user=user)
        name = request.POST.get("name")
        telephone = request.POST.get("telephone")
        address = request.POST.get("address")
        address_tag = request.POST.get("address_tag")
        ret = len(Shipping_address.objects.filter(customer=customer))
        s = Shipping_address(customer=customer, name=name, telephone=telephone, address=address, address_tag=address_tag)
        s.save()
        return JsonResponse({"id": ret})


def data(request, id):
    rlist = [['Jack', 'Chinese'], ['Mike', 'English'], ['Bob', 'Math'], ['Frank', 'Art'], ['Lucy', 'Music']]
    rlist2 = [{"name": rlist[int(id)][0], "subject": rlist[int(id)][1]}]
    rjson = json.dumps(rlist2)
    response = HttpResponse()
    response['Content-Type'] = "text/javascript"
    response.write(rjson)
    return response


def update(request):
    return render_to_response('rubbish.html')


def test(request):
    ret_lists = [
        ['product', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'],
        # ['Cheese Cocoa', 24.1, 0, 79.5, 86.4, 65.2, 82.5],
        # ['梁泽荣', 243.1, 30, 739.5, 863.4, 635.2, 823.5],
        # ['Wa`lnut Brownie', 55.2, 67.1, 69.2, 72.4, 53.9, 39.1]
    ]
    staffs = Staff.objects.all()
    ret_staffs = []
    for staff in staffs:
        ls = [staff.staff_name]
        total_sum = 0
        for year in range(2010, 2021):
            sum = 0
            try:
                begin = datetime.date(year, 1, 1)
                end = datetime.date(year+1, 1, 1)
                sales = Sales.objects.filter(staff=staff, date__range=(begin, end))
                print(sales)
                for sale in sales:
                    sum += sale.sales_amount
            except:
                pass
            ls.append(sum)
            total_sum += sum
        ret_lists.append(ls)
        ret_staffs.append({
            "id": staff.id,
            "staff_name": staff.staff_name,
            "telephone": staff.telephone,
            "gender": staff.gender,
            "position": staff.position,
            "salary": staff.salary,
            "entry_date": staff.entry_date,
            "total_sum": total_sum
        })
    print(ret_lists)
    ret = {
        "lists": ret_lists,
        "staffs": ret_staffs
    }
    return render(request, "display1.html", ret)


@login_required
def init(request):
    try:
        names = ["Foreseen", "long time", "x=2(a+1)"]
        names = ["0ng"]
        # for name in names:
        #     user = User(username=name)
        #     user.set_password(123456)
        #     user.save()
        #     staff = Staff(user=user, staff_name=name, telephone="136****7045", gender="男",
        #           address="深圳大学", position="员工", salary=30000, entry_date="2018-09-01", resignation_date="2020-07-01",
        #           birthday="2000-01-01")
        #     staff.save()
        pass

        # a1 = (2010, 1, 1, 0, 0, 0, 0, 0, 0)  # 设置开始日期时间元组（1976-01-01 00：00：00）
        # a2 = (2019, 12, 31, 23, 59, 59, 0, 0, 0)  # 设置结束日期时间元组（1990-12-31 23：59：59）
        #
        # start = time.mktime(a1)  # 生成开始时间戳
        # end = time.mktime(a2)  # 生成结束时间戳
        # # 随机生成10个日期字符串
        # for i in range(1000):
        #     t = random.randint(start, end)  # 在开始和结束时间戳中随机取出一个
        #     date_touple = time.localtime(t)  # 将时间戳生成时间元组
        #
        #     date = time.strftime("%Y-%m-%d", date_touple)  # 将时间元组转成格式化字符串（1976-05-21）
        #     date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        #     date_end = date + datetime.timedelta(days=1)
        #     name = random.choice(names)
        #     user = User.objects.get(username=name)
        #     staff = Staff.objects.get(user=user)
        #     try:
        #         sales = Sales.objects.filter(staff=staff, date__range=(date, date_end))
        #         sales = sales[0]
        #     except:
        #         sales = Sales(staff=staff, date=date, sales_amount=0)
        #     pre = sales.sales_amount
        #     sales.sales_amount = pre + random.randint(100, 10000)
        #     sales.save()


        # commoditys = Commodity.objects.all()
        # for commodity in commoditys:
        #     commodity.sales = random.randint(10000, 30000)
        #     commodity.save()
    except:
        pass
    return render(request, "index.html")


class employee_performance_analysis(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "员工业绩分析"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面

        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了
        ret_lists = [
            ['product', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020'],
            # ['梁泽荣', 243.1, 30, 739.5, 863.4, 635.2, 823.5],
        ]
        staffs = Staff.objects.all()
        ret_staffs = []
        for staff in staffs:
            ls = [staff.staff_name]
            total_sum = 0
            for year in range(2010, 2021):
                sum = 0
                try:
                    begin = datetime.date(year, 1, 1)
                    end = datetime.date(year+1, 1, 1)
                    sales = Sales.objects.filter(staff=staff, date__range=(begin, end))
                    for sale in sales:
                        sum += sale.sales_amount
                except:
                    pass
                ls.append(sum)
                total_sum += sum
            ret_lists.append(ls)
            ret_staffs.append({
                "id": staff.id,
                "staff_name": staff.staff_name,
                "telephone": staff.telephone,
                "gender": staff.gender,
                "position": staff.position,
                "salary": staff.salary,
                "entry_date": staff.entry_date,
                "total_sum": total_sum
            })
        context["ret_lists"] = ret_lists
        return render(request, "performance.html", context)



class sales_performance_analysis(CommAdminView):
    def get(self, request):
        context = super().get_context()  # 这一步是关键，必须super一下继承CommAdminView里面的context，不然侧栏没有对应数据，我在这里卡了好久
        title = "商品销量分析"  # 定义面包屑变量
        context["breadcrumbs"].append({'url': '/cwyadmin/', 'title': title})  # 把面包屑变量添加到context里面
        context["title"] = title  # 把面包屑变量添加到context里面

        # 下面你可以接着写你自己的东西了，写完记得添加到context里面就可以了

        products = []
        commoditys = Commodity.objects.all()
        sales = []
        for commodity in commoditys:
            products.append(commodity.name)
            sales.append(commodity.sales)
        # for commodity in commoditys:
        #     sales.append(commodity.sales)

        num = len(products)
        datas = []
        for i in range(num):
            datas.append({
                "name": products[i],
                "sale": sales[i]
            })
        context["products"] = products
        context["sales"] = sales
        context["datas"] = datas
        return render(request, "display1.html", context)
