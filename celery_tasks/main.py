from celery_tasks.tasks import build_staic_html


if __name__ == '__main__':
    build_staic_html.delay()


