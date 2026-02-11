const { Client, GatewayIntentBits, SlashCommandBuilder, REST, Routes } = require('discord.js');
const client = new Client({ intents: [GatewayIntentBits.Guilds] });

const TOKEN = process.env.TOKEN;
const CLIENT_ID = process.env.CLIENT_ID;

let data = {}; // lưu điểm theo ID

// ===== Tạo slash commands =====
const commands = [
  new SlashCommandBuilder()
    .setName('add')
    .setDescription('Cộng điểm cho ID')
    .addStringOption(option =>
      option.setName('id')
        .setDescription('Nhập ID')
        .setRequired(true))
    .addIntegerOption(option =>
      option.setName('diem')
        .setDescription('Nhập điểm trận')
        .setRequired(true)
    ),

  new SlashCommandBuilder()
    .setName('bxh')
    .setDescription('Xem bảng xếp hạng')
].map(cmd => cmd.toJSON());

const rest = new REST({ version: '10' }).setToken(TOKEN);

(async () => {
  await rest.put(
    Routes.applicationCommands(CLIENT_ID),
    { body: commands }
  );
})();

// ===== Khi bot nhận lệnh =====
client.on('interactionCreate', async interaction => {
  if (!interaction.isChatInputCommand()) return;

  if (interaction.commandName === 'add') {
    const id = interaction.options.getString('id');
    const diem = interaction.options.getInteger('diem');

    if (!data[id]) {
      data[id] = { total: 0, matches: 0 };
    }

    data[id].total += diem;
    data[id].matches += 1;

    let msg = `ID ${id} đã chơi ${data[id].matches} trận.\nTổng điểm: ${data[id].total}`;

    if (data[id].matches === 4) {
      msg += `\n🔥 Đã đủ 4 trận!`;
    }

    if (data[id].matches === 5) {
      msg += `\n🔥 Đã đủ 5 trận!`;
    }

    await interaction.reply(msg);
  }

  if (interaction.commandName === 'bxh') {
    if (Object.keys(data).length === 0) {
      return interaction.reply("Chưa có dữ liệu.");
    }

    let sorted = Object.entries(data)
      .sort((a, b) => b[1].total - a[1].total);

    let text = "🏆 BẢNG XẾP HẠNG 🏆\n";

    sorted.forEach((item, index) => {
      text += `${index + 1}. ID ${item[0]} - ${item[1].total} điểm (${item[1].matches} trận)\n`;
    });

    await interaction.reply(text);
  }
});

client.once('ready', () => {
  console.log('Bot đã online!');
});

client.login(TOKEN);
