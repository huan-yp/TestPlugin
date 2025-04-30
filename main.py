from ncatbot.plugin import BasePlugin, CompatibleEnrollment
from ncatbot.core.message import GroupMessage, PrivateMessage
from ncatbot.utils.logger import get_log

bot = CompatibleEnrollment  # 兼容回调函数注册器
_log = get_log()

class TestPlugin(BasePlugin):
    name = "TestPlugin" # 插件名称
    version = "0.0.7" # 插件版本

    @bot.group_event()
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        _log.info(f"收到群聊消息: {msg.raw_message}")
        if msg.raw_message == "测试":
            await self.api.post_group_msg(msg.group_id, text="Ncatbot 插件(3.8.x)群聊测试成功喵~")

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):
        _log.info(f"收到私聊消息: {msg.raw_message}")
        if msg.raw_message == "测试":
            await msg.reply("NcatBot 插件私聊测试成功喵~")

    async def on_load(self):
        # 插件加载时执行的操作, 可缺省
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")
        self.register_config("info", "测试配置项")
        self.register_user_func("测试用户功能", self.test_user_func, prefix="/tu")
        self.register_admin_func("测试管理员功能", self.test_admin_func, prefix="/ta")
        
    def test_user_func(self, msg: PrivateMessage):
        msg.reply_sync(text="用户功能:" + self.data['config']['info'])
    
    async def test_admin_func(self, msg: GroupMessage):
        await msg.reply(text="管理员功能(测试热重载):" + self.data['config']['info'])
    
    async def on_unload(self):
        print(f"{self.name} 插件已卸载")
        