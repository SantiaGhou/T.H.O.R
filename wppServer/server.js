const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));
const app = express();

app.use(express.json());

const client = new Client({
    authStrategy: new LocalAuth()
});

const autoChats = new Set();

client.on('qr', (qr) => {
    qrcode.generate(qr, { small: true });
    console.log('Escaneie o QR Code no WhatsApp!');
});

client.on('ready', () => {
    console.log('Bot WhatsApp pronto!');
});

client.on('message', async msg => {
    const chat = await msg.getChat();
    // Só responde se auto-resposta ativada
    if (autoChats.has(chat.name.toLowerCase())) {
        try {
            const resp = await fetch('http://localhost:3002/auto_reply', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contato: chat.name,
                    mensagem: msg.body
                })
            });
            const resposta = await resp.text();
            if (resposta && resposta.trim()) {
                msg.reply(resposta);
            }
        } catch (e) {
            console.log('[X] Erro na auto-reply:', e);
        }
    }
});

// Envio manual
app.post('/enviar', async (req, res) => {
    const { contato, mensagem } = req.body;
    try {
        let chats = await client.getChats();
        let target = chats.find(c =>
            c.name && c.name.toLowerCase() === contato.toLowerCase()
        );
        if (!target) {
            let contacts = await client.getContacts();
            target = contacts.find(c =>
                c.name && c.name.toLowerCase() === contato.toLowerCase()
            );
        }
        if (!target) return res.status(404).send('Contato não encontrado!');
        await client.sendMessage(target.id._serialized, mensagem);
        res.send('Mensagem enviada!');
    } catch (err) {
        res.status(500).send('Erro ao enviar: ' + err);
    }
});

// Ativar/desativar auto-resposta
app.post('/auto_resposta', (req, res) => {
    const { contato, acao } = req.body;
    if (acao === 'ativar') {
        autoChats.add(contato.toLowerCase());
        res.send('Auto-resposta ativada para ' + contato);
    } else if (acao === 'desativar') {
        autoChats.delete(contato.toLowerCase());
        res.send('Auto-resposta desativada para ' + contato);
    } else {
        res.status(400).send('Ação desconhecida');
    }
});

app.listen(3001, () => {
    console.log('API ouvindo na porta 3001');
});
