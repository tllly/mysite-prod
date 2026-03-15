#!/bin/bash

# --- 自动化部署脚本 ---

# 1. 进入项目目录 (根据你的实际路径修改)
# cd /home/tangli/my-project/mysite

# 2. 激活虚拟环境
source venv/bin/activate

# 3. 拉取最新代码 (前提是你已经配置了 Git)
# git pull origin main

# 4. 安装/更新依赖
pip install -r requirements.txt

# 5. 运行数据库迁移
python manage.py migrate --noinput

# 6. 收集静态资源 (WhiteNoise 会处理它们)
# 注意：这会应用 production 设置
export DJANGO_SETTINGS_MODULE=mysite.settings.production
python manage.py collectstatic --noinput

# 7. 重启 Gunicorn 服务 (稍后我们会配置这个服务)
sudo systemctl restart mysite.service

echo "✅ 部署完成！你的外贸网站已更新并运行中。"
