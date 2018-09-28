# Generated by Django 2.1.1 on 2018-09-28 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='账号名称', max_length=50)),
                ('open_id', models.CharField(help_text='账号openID', max_length=50, unique=True)),
                ('token_id', models.CharField(help_text='账号token', max_length=50)),
                ('app_id', models.CharField(help_text='账号ID', max_length=50)),
                ('app_secret', models.CharField(help_text='账号密钥', max_length=255)),
                ('related_url', models.CharField(help_text='关联的url地址', max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'account',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='资源分类名称', max_length=50, unique=True)),
                ('account', models.ForeignKey(help_text='关联账号', on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='wechat.Account')),
            ],
            options={
                'db_table': 'category',
            },
        ),
        migrations.CreateModel(
            name='Keywords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='关键字名称', max_length=50)),
            ],
            options={
                'db_table': 'keywords',
            },
        ),
        migrations.CreateModel(
            name='ManageUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('qrcode', models.ImageField(upload_to='user_qrcode')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(help_text='关联账号', on_delete=django.db.models.deletion.CASCADE, related_name='manageUsers', to='wechat.Account')),
            ],
            options={
                'db_table': 'manage_user',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(help_text='消息类型')),
                ('content', models.CharField(help_text='消息内容', max_length=1000)),
                ('account', models.ForeignKey(help_text='关联账号', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='wechat.Account')),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='ResourceKeywordsMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('keyword', models.ForeignKey(help_text='关联关键字', on_delete=django.db.models.deletion.CASCADE, related_name='resource_keywords_map', to='wechat.Keywords')),
            ],
            options={
                'db_table': 'resource_keywords_map',
            },
        ),
        migrations.CreateModel(
            name='Resources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='资源名称', max_length=50)),
                ('image', models.ImageField(help_text='资源图片', null=True, upload_to='resource_imgs')),
                ('type', models.IntegerField(help_text='资源类型')),
                ('description', models.TextField(help_text='资源描述', null=True)),
                ('share_url', models.CharField(help_text='分享链接', max_length=255)),
                ('share_password', models.CharField(help_text='分享码', max_length=36)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='关联分类', on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='wechat.Category')),
            ],
            options={
                'db_table': 'resources',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('open_id', models.CharField(max_length=50)),
                ('free_count', models.IntegerField(help_text='免费使用额度')),
                ('buy_count', models.IntegerField(default=0, help_text='购买使用额度')),
                ('status', models.IntegerField(default=1, help_text='用户状态')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(help_text='关联账号', on_delete=django.db.models.deletion.CASCADE, related_name='users', to='wechat.Account')),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='resourcekeywordsmap',
            name='resource',
            field=models.ForeignKey(help_text='关联资源', on_delete=django.db.models.deletion.CASCADE, related_name='resource_keywords_map', to='wechat.Resources'),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(help_text='消息用户', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='wechat.User'),
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('account', 'open_id')},
        ),
    ]