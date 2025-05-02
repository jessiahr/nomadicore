from nicegui import ui, run
from fastapi import FastAPI
import psutil
import ollama
from tools import Downloader
import os
from kiwix import update_zim_index, get_zim_index, kiwix_library_path
def main_menu(ui):
    with ui.button(icon='menu').classes('fixed top-4 right-4 z-50'):
        with ui.menu() as menu:
            ui.menu_item('Services', lambda: ui.navigate.to("/"))
            ui.separator()
            ui.menu_item('CPU Stats', lambda: ui.navigate.to("/stats"))

def init(fastapi_app: FastAPI):

    @ui.page('/models')
    def models_page():
        main_menu(ui)
    
    @ui.page('/manage/kiwix')
    def manage_kiwix_page():
        main_menu(ui)
        ui.label('Manage Kiwix').classes('text-2xl m-4')
        log = ui.log(max_lines=10).classes('w-full h-40')
        log.visible = False
        async def update_index():
            log.clear()
            log.visible = True
            log.push('Updating ZIM index...')
            try:
                await run.io_bound(update_zim_index,log.push)
                log.push('ZIM index updated successfully.')
            except Exception as e:
                log.push(f'Error updating ZIM index: {e}')
        with ui.row().classes('flex-wrap gap-4 justify-start p-4') as manage_row:
            ui.button('Update ZIM Index', on_click=update_index).props('outline')
        async def download_zim(zim, progress_bar):
            progress_bar.visible = True
            target_path = os.path.join(kiwix_library_path(), f"{zim['title']}.zim")
            def update_progress(p):
                progress_bar.value = p
            downloader = Downloader(zim['zim_url'], target_path, progress_callback=update_progress)
            await run.io_bound(downloader.download)
        with ui.row().classes('flex-wrap gap-4 justify-start p-4'):
            for zim in get_zim_index():
                with ui.card().classes('w-72 shadow-lg hover:shadow-xl transition-shadow duration-300'):
                    ui.label(zim['title']).classes('text-xl font-semibold')
                    ui.label(zim['summary']).classes('text-sm text-gray-500 mb-2')
                    progress_bar = ui.linear_progress()
                    progress_bar.visible = False
                    ui.button('Download', on_click=lambda zim=zim, progress_bar=progress_bar: download_zim(zim, progress_bar)).props('outline')




    @ui.page('/stats')
    def stats_page():
        main_menu(ui)
        ui.label('System Stats (Per-Core CPU Usage)').classes('text-2xl m-4')
        cpu_widgets = []
        with ui.row().classes('p-4 w-full'):
            mem_label = ui.label()
            mem_progress = ui.linear_progress().props('color=green').classes('w-full ')
        with ui.row().classes('flex-wrap gap-4 justify-start p-4'):
            for i in range(psutil.cpu_count(logical=True)):
                with ui.row().classes('items-center gap-4 w-1/2 max-w-lg'):
                    label = ui.label(f"Core {i}: 0%").classes('w-24')
                    progress = ui.linear_progress().props('striped color=blue').classes('w-full')
                    cpu_widgets.append((label, progress))

        def update_stats():
            core_usages = psutil.cpu_percent(percpu=True)
            for i, usage in enumerate(core_usages):
                label, progress = cpu_widgets[i]
                label.text = f"Core {i}: {usage}%"
                progress.value = usage / 100

            mem = psutil.virtual_memory()
            mem_label.text = f"Memory Usage: {mem.percent}% ({mem.used // (1024 ** 2)}MB / {mem.total // (1024 ** 2)}MB)"
            mem_progress.value = mem.percent / 100

        ui.timer(1.0, update_stats)
    @ui.page('/')
    def home():
        main_menu(ui)
        services = [
            {
                'name': 'Kiwix',
                'description': 'Offline Wikipedia and ZIM file server.',
                'url': 'http://localhost:4000',
            },
            {
                'name': 'Ollama',
                'description': 'Local LLM inference engine.',
                'url': 'http://localhost:11434',
            },
            {
                'name': 'OpenWebUI',
                'description': 'Web interface for local LLMs.',
                'url': 'http://localhost:3000',
            },
            {
                'name': 'Calibre-Web',
                'description': 'Web app for browsing, reading, and managing eBooks.',
                'url': 'http://localhost:8083',
            },
            {
                'name': 'Heimdall',
                'description': 'Web dashboard for managing local services.',
                'url': 'http://localhost:8080',
            },
            {
                'name': 'TileServer GL',
                'description': 'Offline vector tiles server for maps.',
                'url': 'http://localhost:3001',
            },
            {
                'name': 'JupyterLab',
                'description': 'Interactive notebooks and data science IDE.',
                'url': 'http://localhost:8888?token=docker',
            },
            {
                'name': 'Obsidian',
                'description': 'Self-hosted markdown knowledge base.',
                'url': 'http://localhost:3005',
            },
        ]

        ui.label('Nomadicore').classes('text-2xl m-4')

        with ui.row().classes('flex-wrap gap-4 justify-start p-4'):
            for service in services:
                with ui.card().classes('w-72 shadow-lg hover:shadow-xl transition-shadow duration-300'):
                    ui.label(service['name']).classes('text-xl font-semibold')
                    ui.label(service['description']).classes('text-sm text-gray-500 mb-2')
                    ui.button('Open', on_click=lambda url=service['url']: ui.navigate.to(url)).props('outline')

    ui.run_with(
        fastapi_app,
        mount_path='/',  
        storage_secret='pick your private secret here',  # TODO: use a secure secret for production
    )
    