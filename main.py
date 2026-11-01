import os
import asyncio
from aiohttp import web
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View, Select

# ==============================================================================
#  ОБЩИЙ ВЕБ-СЕРВЕР ДЛЯ МОНИТОРИНГА 24/7 (Легкий и стабильный aiohttp)
# ==============================================================================
async def handle(request):
    return web.Response(text="Все 3 Discord-бота успешно работают 24/7!")

async def start_webserver():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"[Успешно] Веб-сервер мониторинга запущен на порту {port}")

# ==============================================================================
#  НАСТРОЙКИ И ИНИЦИАЛИЗАЦИЯ ИНТЕНТОВ ДЛЯ ВСЕХ 3 БОТОВ
# ==============================================================================
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Создаем трех независимых ботов
bot1 = commands.Bot(command_prefix="!", intents=intents) # Бот №1 (Правила)
bot2 = commands.Bot(command_prefix="!", intents=intents) # Бот №2 (Тикеты / Неактив)
bot3 = commands.Bot(command_prefix="!", intents=intents) # Бот №3 (Приветствия новичков)

# ==============================================================================
#  КОНСТАНТЫ ИДЕНТИФИКАТОРОВ (ID КАНАЛОВ И РОЛЕЙ ИЗ ВАШЕГО КОДА)
# ==============================================================================
RULES_CHANNEL_ID = 1559140153782435900   # Канал правил (Бот 1 and Бот 3)
MOD_CHANNEL_ID = 1558487534835605595     # Куда летят тикеты (Бот 2)
SERVER_ID = 1537430503832031315          # ID сервера (Бот 3)
ROLE_ID = 1558480819792912474            # Роль новичка (Бот 3)
WELCOME_CHANNEL_ID = 1537430506004553750 # Канал приветствий (Бот 3)
TICKETS_CHANNEL_ID = 1558476134968983673 # Канал с тикетами (Бот 3)
# ==============================================================================
#  ДАННЫЕ БОТА №1: СЛОВАРЬ ПРАВИЛ И СТРАНИЦ
# ==============================================================================
DISCORD_RULES = (
    "📜 **ПРАВИЛА DISCORD СЕРВЕРА**\n\n"
    "• **1.** Оскорбление участников банды — **Наказание: КИК.**\n"
    "• **2.** Спам в чат банды — **Наказание: ВЫГОВОР.**\n"
    "• **3.** Реклама в чат банды — **Наказание: ВЫГОВОР.**\n"
    "• **4.** Несоблюдение приказов старших по званию — **Наказание: ВЫГОВОР.**\n"
    "• **5.** Сломали машину и не починили, при выяснении кто это сделал участнику будет — **Наказание: ВЫГОВОР.**"
)

RADMIR_PAGES = {
    "ugon": [
        "🚖 **ПРАВИЛА УГОНА ТРАНСПОРТНЫХ СРЕДСТВ (ТС)**\n📄 *Страница 1 из 4*\n\n📊 **ОБЩАЯ ИНФОРМАЦИЯ**\n• 🎲 Угон выдаётся игроку случайным образом при взаимодействии с компьютером на базе банды.\n• ❌ Самостоятельно выбрать конкретное транспортное средство нельзя.\n\n📦 **КАКИЕ ЦЕЛИ МОГУТ БЫТЬ ВЫДАНЫ:**\n• 🏢 Транспортное средство, заспавненное сервером.\n• 👤 ТС другого игрока.\n• 📈 Вероятность получения транспорта зависит от улучшения банды.\n• 💎 **Важно (Премиум угон):** Шанс машин среднего/высокого класса — значительно вырастает.\n• ⚖️ Доступность авто среднего класса остаётся немного выше, чем эконом- и высокого.",
        "🚖 **ПРАВИЛА УГОНА ТРАНСПОРТНЫХ СРЕДСТВ (ТС)**\n📄 *Страница 2 из 4*\n\n🗺️ **ПОИСК И НАЧАЛО УГОНА**\n1. 📞 После получения заказа игроку предлагается осмотреть ТС, которое необходимо угнать.\n2. ⏱️ На осмотр автомобиля предоставляется 1 минута.\n3. 💻 Осмотр можно начать непосредственно у компьютера на базе банды. Повторный осмотр также доступен, однако между ними действует время ожидания.\n4. 📍 После осмотра на карте появляется мигающая ганг-зона, внутри которой находится нужное авто.\n5. 🔍 Район поиска зависит от улучшений банды. Покупка улучшений позволяет уменьшить область поиска автомобиля.\n6. ⏳ На выполнение всего заказа предоставляется 30 минут.",
        "🚖 **ПРАВИЛА УГОНА ТРАНСПОРТНЫХ СРЕДСТВ (ТС)**\n📄 *Страница 3 из 4*\n\n🚔 **ВНИМАНИЕ: ПОЛИЦИЯ И ДРУГИЕ ИГРОКИ**\n• 🚨 Угон автомобиля является частью криминальной системы и связан с процессом поиска и последующей сдачи угнанного ТС.\n• 🚨 Начало угона транспортного средства может привлечь внимание сотрудников правоохранительных органов.\n• 🤝 Автомобиль может быть целью нескольких игроков сразу! Выполнить заказ сможет только тот, кто первым начнет угон.\n• 🔴 Как только один игрок начинает угон, у остальных участников эта ганг-зона поиска исчезает.\n\n🛠️ **ЭТАПЫ УГОНА (ПОШАГОВО)**\nДля успешного завершения заказа необходимо последовательно выполнить все этапы угона.\n• 🔑 *Исключение:* Если авто находится с открытыми дверями или ключ уже находится в замке зажигания, соответствующий этап выполнять не требуется.\n\n1️⃣ **Взлом дверей**\n• Для угона необходимо взломать замок дверей ТС.\n• Действие выполняется с использованием отмычек, которые должны быть у вас в инвентаре.\n• После успешного взлома дверей игрок получает доступ к салону автомобиля.",
        "🚖 **ПРАВИЛА УГОНА ТРАНСПОРТНЫХ СРЕДСТВ (ТС)**\n📄 *Страница 4 из 4*\n\n2️⃣ **Взлом системы зажигания**\n• Для запуска двигателя необходимо взломать систему зажигания.\n• На данном этапе также используются предметы из вашего инвентаря.\n• Этот этап является обязательным, независимо от того, находится ли ключ в замке или нет.\n• После успешного взлома зажигания игрок получает возможность продолжить выполнение заказа.\n\n3️⃣ **Перебивка VIN-номера**\n• Для маскировки угнанного авто необходимо перебить его VIN-номер.\n• Перебивка VIN-номера является обязательным этапом.\n• В отличие от предыдущих систем, перебить VIN-номер можно в любом месте.\n• После успешной перебивки игрок может перейти к финальному этапу — сдаче автомобиля.\n\n4️⃣ **Сдача автомобиля**\n• После перебивки VIN-номера игроку назначается случайное место сдачи ТС.\n• Point отображается на карте в виде красного чекпоинта.\n• 🚛 Вам необходимо доставить угнанное авто строго в указанное место.\n\n💵 **НАГРАДА И ВЛИЯНИЕ**\n• 🏁 Прибыв в точку сдачи, необходимо активировать чекпоинт.\n• 💰 В момент успешной сдачи автомобиля игрок получает денежное вознаграждение за выполненный заказ.\n• 📊 Размер вознаграждения не является постоянным и выбирается системой случайным образом (зависит от класса авто).\n• ⛪ Криминальное влияние: За успешно выполненный угон банда получает 5 очков криминального влияния."
    ],
    "robbery_houses": [
        "🏠 **ПРАВИЛА ОГРАБЛЕНИЯ ДОМОВ**\n📄 *Страница 1 из 1*\n\n*Правила ограбления домов устанавливаются системой проекта Радмир.*\n\n1. Разрешено грабить дома только в определенное правилами сервера время.\n2. Категорически запрещено PG при ограблении (изображать героя против оружия).\n3. Запрещено грабить дома без соответствующих текстовых или голосовых отыгровок.\n4. Все участники налета обязаны находиться в масках и иметь при себе оружие."
    ],
    "crime_general": [
        "🏴‍☠️ **ОБЩИЕ ПРАВИЛА КРИМИНАЛЬНЫХ СТРУКТУР**\n📄 *Страница 1 из 2*\n\n• **1.1** Каждый участник капта за бизнес/территорию/особняк обязан записывать видео (откат). Опровержение предоставляется в течение 24 часов в случае жалобы.\n• **1.2** Владельцы особняка имеют право убить игрока на своей территории, если тот не покидает её.\n• **1.3** Запрещено связывать/надевать мешок не с целью похищения/ограбления. | **Наказание: Warn.**\n• **1.4** Многочисленные нарушения от банды за короткий срок. | **Наказание: Warn владельцу банды.**",
        "🏴‍☠️ **ОБЩИЕ ПРАВИЛА КРИМИНАЛЬНЫХ СТРУКТУР**\n📄 *Страница 2 из 2*\n\n• **1.5** Действия, направленные на срыв проведения каптов (убийство у точки за 15 минут до начала и т.д.). | **Наказание: Предупреждение банде.**\n• **1.6** DM со стороны банды. | **Наказание: Деморган 120 мин / Warn / Бан оружия на 360-720 мин.**\n*Примечание:* ДМ крайм/гос разрешен вне города, если нет свидетелей-гражданских.\n• **1.7** Нападение без маски на гос. структуры, задерживающих игроков. | **Наказание: Warn.**\n*Примечание:* спасать в масках можно любого члена любой банды."
    ],
    "capt_rules": [
        "⚔️ **ПРАВИЛА ЗАХВАТА БИЗНЕСОВ/ТЕРРИТОРИЙ/ОСОБНЯКОВ**\n📄 *Страница 1 из 3*\n\n• **2.1** Использование запрещенного оружия на захвате бизнеса/территории/особняка. | **Наказание: Warn.**\n• **2.2** Использование маски и анимаций после 5 минуты (при захвате за особняк — в течение всего времени). | **Наказание: Warn.**\n• **2.3** BH (BunnyHop) во время стрельбы. | **Наказание: Деморган 30 минут.**",
        "⚔️ **ПРАВИЛА ЗАХВАТА БИЗНЕСОВ/ТЕРРИТОРИЙ/ОСОБНЯКОВ**\n📄 *Страница 2 из 3*\n\n• **2.4** Уход в AFK во время захвата. | **Наказание: Kick.**\n• **2.5** После 6-й минуты занимать труднодоступные территории, попасть на которые можно только прыжком или вплавь. | **Наказание: Warn.**\n• **2.6** Любое использование возвышенностей, на которые можно забраться только прыжком. | **Наказание: Warn.**\n• **2.7** Любое использование низменностей, из которых можно выбраться только прыжком. | **Наказание: Warn.**",
        "⚔️ **ПРАВИЛА ЗАХВАТА БИЗНЕСОВ/ТЕРРИТОРИЙ/ОСОБНЯКОВ**\n📄 *Страница 3 из 3*\n\n• **2.8** От одного участника войны за крышу бизнеса/территорию в общее количество нарушений банды засчитывается не более 2 нарушений.\n• **2.9** Запрещено использование скинов, дающих преимущество. | **Наказание: От warn до блокировки игрового аккаунта на 15 дней.**\n• **2.10** Участие в захвате имея пинг 200 и более. | **Наказание: Kick.**"
    ],
    "district_rules": [
        "🏘️ **ПРАВИЛА ЗАХВАТА РАЙОНОВ**\n📄 *Страница 1 из 2*\n\n• **3.1** В качестве т/с запрещены грузовые автомобили и автодома. | **Наказание: Warn.**\n• **3.2** Взаимодействие с транспортным средством после 05:30 на таймере захвата. | **Наказание: Предупреждение банде.**",
        "🏘️ **ПРАВИЛА ЗАХВАТА РАЙОНОВ**\n📄 *Страница 2 из 2*\n\n• **3.3** Использование бронежилетов или аптечек в бою во время удержания районов. | **Наказание: Деморган 60 минут.**\n• **3.4** Стрельба из транспортных средств по участникам захвата. | **Наказание: Warn / Деморган 120 минут.**"
    ]
}
# ==============================================================================
#  ЛОГИКА БОТА №1: ВЫБОР ПРАВИЛ И СТРАНИЦЫ ПАГИНАЦИИ
# ==============================================================================
class RulesSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Правила угона ТС", value="ugon", description="Правила и этапы угона автомобилей", emoji="🚖"),
            discord.SelectOption(label="Ограбление домов", value="robbery_houses", description="Правила налетов на дома", emoji="🏠"),
            discord.SelectOption(label="Общие правила крайм", value="crime_general", description="Основные правила криминала", emoji="🏴‍☠️"),
            discord.SelectOption(label="Захват бизнесов/терр", value="capt_rules", description="Правила каптов и стрел за особняки", emoji="⚔️"),
            discord.SelectOption(label="Захват районов", value="district_rules", description="Правила удержания районов банды", emoji="🏘️")
        ]
        super().__init__(placeholder="📋 Выберите категорию правил...", min_values=1, max_values=1, options=options, custom_id="persistent:rules_select")

    async def callback(self, interaction: discord.Interaction):
        key = self.values[0]
        pages = RADMIR_PAGES.get(key, [])
        if not pages:
            await interaction.response.send_message("Ошибка: Правила не найдены.", ephemeral=True)
            return
        
        view = RulesPaginationView(key, pages, 0)
        await interaction.response.send_message(content=pages[0], view=view, ephemeral=True)


class RulesPaginationView(View):
    def __init__(self, key: str, pages: list, current_page: int):
        super().__init__(timeout=None)
        self.key = key
        self.pages = pages
        self.current_page = current_page
        self.update_buttons()

    def update_buttons(self):
        self.prev_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page == len(self.pages) - 1
        self.page_counter.label = f"{self.current_page + 1}/{len(self.pages)}"

    @discord.ui.button(label="⬅️ Назад", style=discord.ButtonStyle.secondary, custom_id="persistent:rules_prev")
    async def prev_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_buttons()
            await interaction.response.edit_message(content=self.pages[self.current_page], view=self)

    @discord.ui.button(label="1/1", style=discord.ButtonStyle.secondary, disabled=True, custom_id="persistent:rules_counter")
    async def page_counter(self, interaction: discord.Interaction, button: Button):
        pass

    @discord.ui.button(label="Вперед ➡️", style=discord.ButtonStyle.secondary, custom_id="persistent:rules_next")
    async def next_page(self, interaction: discord.Interaction, button: Button):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.update_buttons()
            await interaction.response.edit_message(content=self.pages[self.current_page], view=self)


class MainRulesView(View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RulesSelect())


@bot1.event
async def on_ready():
    bot1.add_view(MainRulesView())
    print(f"[Успешно] Бот №1 (Правила) запущен как {bot1.user}")


@bot1.command(name="setup_rules")
@commands.has_permissions(administrator=True)
async def setup_rules(ctx):
    channel = bot1.get_channel(RULES_CHANNEL_ID)
    if not channel:
        await ctx.send(f"Ошибка: Не удалось найти канал с ID {RULES_CHANNEL_ID}", delete_after=5)
        return

    await channel.send(content=DISCORD_RULES, view=MainRulesView())
    await ctx.send("✅ Меню выбора правил успешно отправлено в целевой канал!", delete_after=5)
    try: await ctx.message.delete()
    except: pass
# ==============================================================================
#  ЛОГИКА БОТА №2: СИСТЕМА ТИКЕТОВ И ЗАЯВЛЕНИЙ НА НЕАКТИВ
# ==============================================================================
class TicketModal(discord.ui.Modal, title="Заполнение тикета"):
    topic = discord.ui.TextInput(label="Тема обращения", placeholder=" Введите ваш игровой НИК ")
    description = discord.ui.TextInput(
        label="Сколько вас не будет в игре?", 
        style=discord.TextStyle.paragraph, 
        placeholder="Опишите причину неактива и сроки как можно подробнее...",
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        mod_channel = interaction.guild.get_channel(MOD_CHANNEL_ID)
        if mod_channel is None:
            await interaction.response.send_message("Ошибка: Канал для руководства не найден.", ephemeral=True)
            return

        embed = discord.Embed(title="🎫 Новое заявление на неактив!", color=discord.Color.green())
        embed.add_field(name="Автор:", value=f"{interaction.user.mention} ({interaction.user})", inline=False)
        embed.add_field(name="Игровой Ник:", value=self.topic.value, inline=False)
        embed.add_field(name="Сроки и описание:", value=self.description.value, inline=False)
        embed.set_footer(text=f"ID пользователя: {interaction.user.id}")

        await mod_channel.send(embed=embed)
        await interaction.response.send_message("Ваше заявление успешно отправлено руководству!", ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Открыть тикет 🎫", style=discord.ButtonStyle.primary, custom_id="persistent_view:ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TicketModal())


@bot2.event
async def on_ready():
    try:
        bot2.add_view(TicketView())
        synced = await bot2.tree.sync()
        print(f"[Успешно] Бот №2 (Тикеты) запущен как {bot2.user}. Синхронизировано команд: {len(synced)}")
    except Exception as e:
        print(f"Ошибка синхронизации Бота 2: {e}")


@bot2.tree.command(name="send_ticket_button", description="Отправить кнопку для создания тикетов")
@app_commands.checks.has_permissions(administrator=True)
async def send_ticket_button(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Поддержка сервера", 
        description="Нажмите на кнопку ниже, чтобы заполнить форму и связаться с администрацией.",
        color=discord.Color.blue()
    )
    await interaction.channel.send(embed=embed, view=TicketView())
    await interaction.response.send_message("Кнопка тикетов успешно отправлена!", ephemeral=True)


@bot2.command(name="кнопка")
@commands.has_permissions(administrator=True)
async def кнопка(ctx):
    embed = discord.Embed(
        title="Заявления на неактив", 
        description="Нажмите на кнопку ниже, чтобы заполнить форму. Данные сразу уйдут руководству.",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=TicketView())
# ==============================================================================
#  ЛОГИКА БОТА №3: ПРИВЕТСТВИЕ НОВИЧКОВ, ВЫДАЧА РОЛЕЙ И СКРЫТЫЕ КНОПКИ
# ==============================================================================
class EphemeralWelcomeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Где правила?", style=discord.ButtonStyle.success, emoji="📜", custom_id="rules_btn")
    async def rules_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content=f"📜 Переходи в канал с правилами: <#{RULES_CHANNEL_ID}>", 
            ephemeral=True
        )

    @discord.ui.button(label="Нужен тикет / Поддержка", style=discord.ButtonStyle.danger, emoji="🎫", custom_id="tickets_btn")
    async def tickets_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            content=f"🎫 Создать тикет или подать на неактив можно в этом канале: <#{TICKETS_CHANNEL_ID}>", 
            ephemeral=True
        )


class MainWelcomeView(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Получить приветственное меню", style=discord.ButtonStyle.blurple, emoji="👋", custom_id="welcome_btn_v2")
    async def welcome_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=f"Добро пожаловать, {interaction.user.name}!",
            description="Рады видеть тебя на сервере! Это меню видишь только ты.\n\n"
                        "Нажми на интересующую кнопку ниже, чтобы получить быструю ссылку на нужный чат.",
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=EphemeralWelcomeView(), ephemeral=True)


@bot3.event
async def on_ready():
    bot3.add_view(MainWelcomeView())
    bot3.add_view(EphemeralWelcomeView())
    print(f"[Успешно] Бот №3 (Приветствия) запущен как {bot3.user}")


@bot3.event
async def on_member_join(member: discord.Member):
    if member.guild.id != SERVER_ID: 
        return
        
    role = member.guild.get_role(ROLE_ID)
    if role:
        try: await member.add_roles(role)
        except Exception as e: print(f"Не удалось выдать роль новичку: {e}")

    welcome_channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if welcome_channel:
        try:
            ping_msg = await welcome_channel.send(f"Привет, {member.mention}! Нажми на синюю кнопку выше 👆, чтобы открыть меню новичка.")
            await asyncio.sleep(15)
            await ping_msg.delete()
        except: pass


@bot3.command(name="setup_welcome")
@commands.has_permissions(administrator=True)
async def setup_welcome(ctx):
    embed = discord.Embed(
        title="Добро пожаловать на наш сервер!",
        description="Новички, нажмите на кнопку ниже, чтобы получить ссылки на правила и поддержку.\n*Содержимое меню откроется скрытно и будет видно только вам.*",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed, view=MainWelcomeView())
    try: await ctx.message.delete()
    except: pass


# ==============================================================================
#  ГЛАВНАЯ ФУНКЦИЯ ОДНОВРЕМЕННОГО ЗАПУСКА ВСЕХ ТРЕХ БОТОВ
# ==============================================================================
async def start_all():
    # 1. Сначала поднимаем общий веб-сервер
    await start_webserver()
    
    # 2. Получаем токены из .env файла или системных переменных
    token1 = os.getenv("BOT_TOKEN_1")
    token2 = os.getenv("BOT_TOKEN_2")
    token3 = os.getenv("BOT_TOKEN_3")

    t1 = token1.strip().strip('"').strip("'") if token1 else None
    t2 = token2.strip().strip('"').strip("'") if token2 else None
    t3 = token3.strip().strip('"').strip("'") if token3 else None

    if not all([t1, t2, t3]):
        print("[Ошибка] В настройках отсутствуют токены! Проверьте переменные BOT_TOKEN_1, BOT_TOKEN_2, BOT_TOKEN_3.")
        return

    # 3. Объединяем асинхронные задачи ботов в один бесконечный цикл
    print("[Старт] Подключение ботов к Discord...")
    await asyncio.gather(
        bot1.start(t1),
        bot2.start(t2),
        bot3.start(t3)
    )

if __name__ == "__main__":
    try:
        asyncio.run(start_all())
    except KeyboardInterrupt:
        print("Работа всех ботов успешно остановлена.")

