from django.contrib import admin

# Register your models here.
from django.db.models import Sum

from .models import Commodity, Staff, Order, Customer, Order_detail
from import_export.admin import ImportExportModelAdmin
# from daterange_filter.filter import DateRangeFilter
from xadmin import views
from xadmin.layout import Main, TabHolder, Tab, Fieldset, Row, Col, AppendedText, Side, Field
import xadmin


# 基础设置
class BaseSetting(object):
    enable_themes = True    # 使用主题
    use_bootswatch = True


# 全局设置
class GlobalSettings(object):
    site_title = '冰酒后台管理系统'  # 标题
    site_footer = '版权所有'  # 页尾
    site_url = '/'
    menu_style = 'accordion'  # 设置左侧菜单  折叠样式

    def get_site_menu(self):  #名称不能改
        return [
            {
                'title': '数据分析',
                'icon': 'fa fa-bar-chart-o',
                'menus': (
                    {
                        'title': '员工业绩分析',    #这里是你菜单的名称
                        'url': '/xadmin/employee_performance_analysis',     #这里填写你将要跳转url
                        'icon': 'fa fa-cny'     #这里是bootstrap的icon类名，要换icon只要登录bootstrap官网找到icon的对应类名换上即可
                    },
                    {
                        'title': '商品销量分析',
                        'url': '/xadmin/sales_performance_analysis',
                        'icon': 'fa fa-cny'
                    }
                )
            }
        ]



class CommodityAdmin(object):
    list_filter = ['sales', 'stock', 'production_date', 'shelf_life']
    list_display = ('id', 'name', 'upload_img', 'purchase_price', 'selling_price', 'sales', 'stock')
    list_display_links = ['name']
    # list_display_link = ('name')
    # redirect = True
    # readonly_fields = ['upload_img']
    search_fields = ['name']
    form_layout = (
        Fieldset(
            '图片',
            Row('img'),
        ),
        Fieldset(
            '产品信息',
            Row('name', 'origin_address'),
            Row('production_date', 'shelf_life'),
            Row('standard'),
            'detail',
        ),
        Fieldset(
            '销售信息',
            Row('purchase_price', 'selling_price'),
            Row('sales', 'stock'),
        ),
    )
    # fieldsets = [
    #     ('图片',     {'fields': ['upload_img']}),
    #     ('产品信息', {'fields': ['name', 'origin_address', 'production_date', 'shelf_life', 'standard', 'detail']}),
    #     ('销售信息',      {'fields': ['purchase_price', 'selling_price', 'sales']}),
    # ]
    ordering = ('id',)
    data_charts = {
        "user_count": {'title': u"Sales", "x-field": "id", "y-field": ("sales",),
                       "order": ('id',)},
        # "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    }


class OrderInline(object):
    model = Order
    # 默认提供三个足够的选项字段
    extra = 3


class Order_detailInline(object):
    model = Order_detail
    extra = 3


class StaffAdmin(object):
    list_filter = ['salary']
    list_display = ('staff_name', 'gender', 'telephone', 'address', 'salary')
    search_fields = ['staff_name']
    inlines = [OrderInline]
    form_layout = (
        Fieldset(
            '基本信息',
            Row('user'),
            Row('staff_name', 'gender'),
            Row('telephone', 'address'),
            Row('birthday'),
        ),
        Fieldset(
            '职位信息',
            Row('position', 'salary'),
            Row('entry_date', 'resignation_date'),
        ),
    )
    # fieldsets = [
    #     ('基本信息', {'fields': ['staff_name', 'telephone', 'gender', 'address', 'birthday']}),
    #     ('职位信息', {'fields': ['position', 'salary', 'entry_date', 'resignation_date']})
    # ]
    ordering = ('id',)


class OrderAdmin(object):
    list_filter = ['order_creation_time', 'customer', 'payment_status']
    list_display = ('customer', 'staff', 'order_creation_time', 'total_amount', 'real_payment')
    search_fields = ['customer__user_name', 'staff__staff_name']
    inlines = [Order_detailInline]
    # 使得DateTimeField对象能够显示在admin中
    readonly_fields = ['order_creation_time']
    form_layout = (
        Fieldset(
            '总体信息',
            Row('order_creation_time'),
            Row('customer'),
            Row('staff'),
        ),
        Fieldset(
            '支付信息',
            Row('total_amount'),
            Row('real_payment', 'payment_method'),
            Row('deposit', 'payment_status'),
            Row('discounted_price'),
        ),
        Fieldset(
            '运送信息',
            Row('name', 'telephone'),
            Row('area', 'address'),
            Row('address_tag'),
            Row('shipping'),
        ),
    )
    # fieldsets = [
    #     ('总体信息', {'fields': ['customer', 'order_creation_time', 'staff']}),
    #     ('支付信息', {'fields': ['total_amount', 'real_payment', 'payment_method', 'discounted_price', 'deposit', 'payment_status']}),
    #     ('运送信息', {'fields': ['name', 'shipping', 'telephone', 'area', 'address', 'address_tag']})
    # ]
    ordering = ('id',)


class CustomerAdmin(object):
    list_display = ('user_name', 'types', 'customer_level', 'consumption_amount')
    search_fields = ['user_name']
    form_layout = (
        Fieldset(
            '基本信息',
            Row('user'),
            Row('user_name'),
            Row('telephone', 'address'),
            Row('contact_person', 'types'),
        ),
        Fieldset(
            '消费信息',
            Row('consumption_amount'),
            Row('total_shopping_cart'),
            Row('customer_level'),
        ),
    )
    list_filter = ['customer_level']
    ordering = ('id',)


xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(Commodity, CommodityAdmin)
xadmin.site.register(Staff, StaffAdmin)
xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(Customer, CustomerAdmin)
# admin.site.register(Order_detail)

#注册GlobalSetting
from luogu.views import employee_performance_analysis   #从你的app的view里引入你将要写的view，你也可以另外写一个py文件，把后台的view集中在一起方便管理
from luogu.views import sales_performance_analysis   #从你的app的view里引入你将要写的view，你也可以另外写一个py文件，把后台的view集中在一起方便管理
xadmin.site.register_view(r'employee_performance_analysis/$', employee_performance_analysis, name='for_test')
xadmin.site.register_view(r'sales_performance_analysis/$', sales_performance_analysis, name='for_test')