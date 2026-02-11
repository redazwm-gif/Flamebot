const { 
  Client, 
  GatewayIntentBits, 
  SlashCommandBuilder, 
  REST, 
  Routes, 
  ModalBuilder, 
  TextInputBuilder, 
  TextInputStyle, 
  ActionRowBuilder 
} = require('discord.js');

const TOKEN = process.env.TOKEN;
const CLIENT_ID = process.env.CLIENT_ID;

const client = new Client({
  intents: [GatewayIntentBits.Guilds]
});

let database = {}; // lưu điểm theo custom

// ===== Đăng ký slash command =====
const commands = [
  new SlashCommandBuilder()
    .setName('tinhdiem')
    .setDescription('Nhập điểm custom'),
  new SlashCommandBuilder()
    .setName('bxh')
    .setDescription('Xem bảng xếp hạng')
    .addStringOption(option =>
      option.setName('custom')
        .setDescription('Nhập id custom')
        .setRequired(true))
].map(cmd => cmd.toJSON());

const rest = new REST({ version: '10' }).setToken(TOKEN);

(async () => {
  await rest.put(
    Routes.applicationCommands(CLIENT_ID),
    { body: commands }
  );
})();

// ===== Xử lý interaction =====
client.on('interactionCreate', async interaction => {

  if (interaction.isChatInputCommand()) {

    // Mở form
    if (interaction.commandName === 'tinhdiem') {

      const modal = new ModalBuilder()
        .setCustomId('formTinhDiem')
        .setTitle('Tính điểm custom');

      const idCustom = new TextInputBuilder()
        .setCustomId('idcustom')
        .setLabel('ID Custom')
        .setStyle(TextInputStyle.Short)
        .setRequired(true);

      const idGame = new TextInputBuilder()
        .setCustomId('idgame')
        .setLabel('ID Người chơi')
        .setStyle(TextInputStyle.Short)
        .setRequired(true);

      const diem = new TextInputBuilder()
        .setCustomId('diem')
        .setLabel('Điểm trận')
        .setStyle(TextInputStyle.Short)
        .setRequired(true);

      modal.addComponents(
        new ActionRowBuilder().addComponents(idCustom),
        new ActionRowBuilder().addComponents(idGame),
        new ActionRowBuilder().addComponents(diem)
      );

      await interaction.showModal(modal);
    }

    // Xem bảng xếp hạng
    if (interaction.commandName === 'bxh') {
      const custom = interaction.options.getString('custom');

      if (!database[custom]) {
        return interaction.reply("Custom này chưa có dữ liệu.");
      }

      let sorted = Object.entries(database[custom])
        .sort((a, b) => b[1] - a[1]);

      let text = `🏆 BXH Custom ${custom} 🏆\n`;

      sorted.forEach((player, index) => {
        text += `${index + 1}. ID ${player[0]} - ${player[1]} điểm\n`;
      });

      await interaction.reply(text);
    }
  }

  // Khi submit form
  if (interaction.isModalSubmit()) {

    if (interaction.customId === 'formTinhDiem') {

      const custom = interaction.fields.getTextInputValue('idcustom');
      const id = interaction.fields.getTextInputValue('idgame');
      const diem = parseInt(interaction.fields.getTextInputValue('diem'));

      if (!database[custom]) {
        database[custom] = {};
      }

      if (!database[custom][id]) {
        database[custom][id] = 0;
      }

      database[custom][id] += diem;

      await interaction.reply(`✅ Đã cộng ${diem} điểm cho ID ${id} trong custom ${custom}`);
    }
  }
});

client.once('ready', () => {
  console.log('Bot đã online!');
});

client.login(TOKEN);
