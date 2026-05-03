# Voice And Media

Use this reference when configuring voice input, voice output, images, or media-related gateway behavior.

## Voice Mode

Inside an interactive session:

```text
/voice on
/voice tts
/voice off
```

Use `/reset` or restart the gateway if voice config changes do not apply.

## STT: Voice To Text

Voice messages from supported gateway platforms can be transcribed before reaching the model.

Common provider choices:

| Provider | Setup | Notes |
| --- | --- | --- |
| Local faster-whisper | `pip install faster-whisper` in Hermes environment | Free, local, CPU/GPU dependent. |
| Groq Whisper | `GROQ_API_KEY` | Often fast; provider availability may vary. |
| OpenAI Whisper | `VOICE_TOOLS_OPENAI_KEY` or provider-specific OpenAI key | Paid. |
| Mistral Voxtral | `MISTRAL_API_KEY` | Provider-specific. |

Example config shape:

```yaml
stt:
  enabled: true
  provider: local
  local:
    model: base
```

Validate with:

```bash
hermes config check
hermes doctor
```

## TTS: Text To Speech

Common providers:

| Provider | Env/config | Notes |
| --- | --- | --- |
| Edge TTS | no API key | Common default/free option. |
| ElevenLabs | `ELEVENLABS_API_KEY` | Free tier/premium voices. |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | Paid. |
| MiniMax | `MINIMAX_API_KEY` | Paid. |
| Mistral Voxtral | `MISTRAL_API_KEY` | Paid/provider-specific. |
| NeuTTS local | local dependencies such as `neutts` and `espeak-ng` | Free but heavier setup. |

Set provider through `hermes setup tts`, `hermes config edit`, or `hermes config set` if exact keys are known from current help/docs.

## Images

Single-query local image input can be available through:

```bash
hermes chat -q "Describe this image" --image ./image.png
```

Inside CLI, `/image` may attach a local image and `/paste` may attach a clipboard image where supported.

## Media Troubleshooting

Voice not working:

1. Check `stt.enabled` and the configured provider.
2. Check required env vars in `.env`.
3. Check gateway logs with `hermes logs --component gateway --since 1h`.
4. Restart CLI/gateway after config changes.
5. Verify the platform supports sending voice/audio attachments to the bot.

TTS not working:

1. Check TTS provider env vars.
2. Try Edge TTS or another known-good provider.
3. Verify outbound media/file permissions on the gateway platform.
4. Inspect `hermes logs errors`.

Image input not working:

1. Check `hermes chat --help` for `--image`.
2. Confirm file path exists and is readable.
3. Ensure vision/image toolsets are enabled when needed.
4. Restart or `/reset` after tool changes.
