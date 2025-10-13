from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=50, verbose_name='用户名')
    email = models.EmailField(verbose_name='邮箱地址', max_length=50)
    password = models.CharField(verbose_name='密码', max_length=50)


class PricePolicy(models.Model):
    # 价格策略
    category_chose = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    category = models.SmallIntegerField(verbose_name='收费类型', default=2, choices=category_chose)
    title = models.CharField(verbose_name='标题', max_length=50)
    price = models.PositiveIntegerField(verbose_name='价格')
    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    project_space = models.PositiveIntegerField(verbose_name='单个项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    # 交易记录
    status_choice = (
        (1, '已支付'),
        (2, '未支付'),
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)

    order = models.CharField(verbose_name='订单号', max_length=50, unique=True)

    user = models.ForeignKey(verbose_name='用户', to=UserInfo, on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name='价格策略', to=PricePolicy, on_delete=models.CASCADE)

    count = models.IntegerField(verbose_name='数量(年)', help_text='0表示无期限')

    price = models.IntegerField(verbose_name='实际支付价格')

    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)

    create_datetime = models.DateTimeField(auto_now_add=True)


class Project(models.Model):
    # 项目表
    COLOR_CHOICES = (
        (1, '#A7CE4F'),
        (2, '#E7DA96'),
        (3, '#9EBAC6'),
        (4, '#F79A57'),
        (5, '#EB4A59'),
        (6, '#5E595A'),
        (7, '#BA55D3'),
    )
    name = models.CharField(verbose_name='项目名', max_length=50)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    use_space = models.IntegerField(verbose_name='项目已使用空间', default=0)
    start = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to=UserInfo, on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # 腾讯cos桶
    bucket = models.CharField(verbose_name="cos桶", max_length=128)
    region = models.CharField(verbose_name="cos区",max_length=32)


class ProjectUser(models.Model):
    """项目参与者"""
    project = models.ForeignKey(verbose_name='项目', to=Project, on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='参与者', to=UserInfo, on_delete=models.CASCADE)

    start = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)


class Wiki(models.Model):
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=50)
    content = models.TextField(verbose_name='内容')

    # 自关联
    parent = models.ForeignKey(verbose_name='父文章', to='Wiki', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='children')

    # 深度
    depth = models.IntegerField(verbose_name='深度', default=1)

    def __str__(self):
        return self.title


class FileRepository(models.Model):
    """文件库"""
    project = models.ForeignKey(verbose_name='项目名', to='Project', on_delete=models.CASCADE)
    file_type_choices = (
        (1,'文件'),
        (2,'文件夹'),
    )
    file_type = models.SmallIntegerField(verbose_name='文件类型', choices=file_type_choices)
    name = models.CharField(verbose_name='文件夹名称', max_length=50,help_text='文件/文件夹名')
    key = models.CharField(verbose_name='文件存储在cos中的key', max_length=128,null=True, blank=True)
    file_size = models.IntegerField(verbose_name='文件大小', null=True, blank=True)
    file_path = models.CharField(verbose_name='文件路路径', max_length=256, null=True, blank=True)
    parent = models.ForeignKey(verbose_name='父级目录',to='self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    update_user = models.ForeignKey(verbose_name='最近更新者', to=UserInfo, on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
