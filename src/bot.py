import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from database.core import Core


bot = Bot(token="7160912860:AAHSnw7Vj5sW9uc5u4wJCSyTd2FJOkdGJhM")
dp = Dispatcher()
db = Core()


@dp.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer("Hello, user!")

@dp.message(Command("add"))
async def command_add(message: Message) -> None:
    task_name: str = " ".join(message.text.split()[1:])
    message_author_id: str = str(message.from_user.id)

    await db.add_task(task_name, message_author_id)
    await message.answer("Ваша задача успешно добавлена в БД!")

@dp.message(Command("tsk"))
async def command_tsk(message: Message) -> None:
    tasks = await db.get_tasks()
    tasks_amount: int = len(tasks)
    text = "Список задач:\n"

    if tasks_amount == 0:
        await message.answer("Список задач пуст!")
        return

    for task_index in range(0, tasks_amount):
        id: int = tasks[task_index][0]
        name: str = tasks[task_index][1]
        creator_id: str = tasks[task_index][2]
        task_text: str = f"[{id}] {name}, ID-автора - {creator_id}"

        if task_index + 1 != tasks_amount:
            task_text += "\n"
        
        text += task_text

    await message.answer(text)


async def main():
    await Core.create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())