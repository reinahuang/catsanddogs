FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# 使用 python -m pip 保证 pip 与运行时的 python 是同一个解释器
RUN python -m pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY app.py .

EXPOSE 80

CMD ["python", "app.py"]