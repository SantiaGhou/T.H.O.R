const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const app = express();

app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth()
});

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneie o QR Code no WhatsApp!');
});

client.on('ready', () => {
    console.log('Bot WhatsApp pronto!');
});

client.initialize();

app.post('/enviar', async (req, res) => {
    const { contato, mensagem } = req.body;
    try {
        // Busca em chats recentes
        let chats = await client.getChats();
        let target = chats.find(c =>
            c.name &&
            c.name.toLowerCase() === contato.toLowerCase()
        );

        // Se não achou, tenta busca aproximada (contém o nome)
        if (!target) {
            let similares = chats
                .filter(c => c.name && c.name.toLowerCase().includes(contato.toLowerCase()))
                .map(c => c.name);
            if (similares.length) {
                return res.status(404).json({
                    erro: 'Contato não encontrado exatamente.',
                    sugestoes: similares
                });
            }
        }

        // Busca em contatos se não achou em chats
        if (!target) {
            let contacts = await client.getContacts();
            target = contacts.find(c =>
                c.name &&
                c.name.toLowerCase() === contato.toLowerCase()
            );
            // Busca por aproximação também nos contatos
            if (!target) {
                let similares = contacts
                    .filter(c => c.name && c.name.toLowerCase().includes(contato.toLowerCase()))
                    .map(c => c.name);
                if (similares.length) {
                    return res.status(404).json({
                        erro: 'Contato não encontrado exatamente.',
                        sugestoes: similares
                    });
                }
            }
        }

        // Se ainda não encontrou, retorna erro
        if (!target) return res.status(404).send('Contato não encontrado!');

        await client.sendMessage(target.id._serialized, mensagem);
        res.send('Mensagem enviada!');
    } catch (err) {
        res.status(500).send('Erro ao enviar: ' + err);
    }
});

app.listen(3001, () => {
    console.log('API ouvindo na porta 3001');
});
