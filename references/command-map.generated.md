# Hermes CLI Help Snapshot

Generated from local `hermes --help` and `hermes <command> --help`.
Regenerate with `scripts/hermes_check.py --write-help references/command-map.generated.md`.

## Root

```text
usage: hermes [-h] [--version] [-z PROMPT] [-m MODEL] [--provider PROVIDER] [-t TOOLSETS] [--resume SESSION] [--continue [SESSION_NAME]] [--worktree] [--accept-hooks] [--skills SKILLS] [--yolo] [--pass-session-id] [--ignore-user-config] [--ignore-rules] [--tui] [--dev] {chat,model,fallback,gateway,setup,whatsapp,slack,login,logout,auth,status,cron,webhook,kanban,hooks,doctor,dump,debug,backup,import,config,pairing,skills,plugins,curator,memory,tools,mcp,sessions,insights,claw,version,update,uninstall,acp,profile,completion,dashboard,logs} ...
```

## Commands

| Command | Usage | Subcommands |
| --- | --- | --- |
| `chat` | `usage: hermes chat [-h] [-q QUERY] [--image IMAGE] [-m MODEL] [-t TOOLSETS] [-s SKILLS] [--provider PROVIDER] [-v] [-Q] [--resume SESSION_ID] [--continue [SESSION_NAME]] [--worktree] [--accept-hooks] [--checkpoints] [--max-turns N] [--yolo] [--pass-session-id] [--ignore-user-config] [--ignore-rules] [--source SOURCE] [--tui] [--dev]` | - |
| `model` | `usage: hermes model [-h] [--portal-url PORTAL_URL] [--inference-url INFERENCE_URL] [--client-id CLIENT_ID] [--scope SCOPE] [--no-browser] [--timeout TIMEOUT] [--ca-bundle CA_BUNDLE] [--insecure]` | - |
| `fallback` | `usage: hermes fallback [-h] {list,ls,add,remove,rm,clear} ...` | list, ls, add, remove, rm, clear |
| `gateway` | `usage: hermes gateway [-h] [--accept-hooks] {run,start,stop,restart,status,install,uninstall,setup,migrate-legacy} ...` | run, start, stop, restart, status, install, uninstall, setup, migrate-legacy |
| `setup` | `usage: hermes setup [-h] [--non-interactive] [--reset] [--reconfigure] [--quick] [{model,tts,terminal,gateway,tools,agent}]` | model, tts, terminal, gateway, tools, agent |
| `whatsapp` | `usage: hermes whatsapp [-h]` | - |
| `slack` | `usage: hermes slack [-h] {manifest} ...` | manifest |
| `login` | `usage: hermes login [-h] [--provider {nous,openai-codex}] [--portal-url PORTAL_URL] [--inference-url INFERENCE_URL] [--client-id CLIENT_ID] [--scope SCOPE] [--no-browser] [--timeout TIMEOUT] [--ca-bundle CA_BUNDLE] [--insecure]` | nous, openai-codex |
| `logout` | `usage: hermes logout [-h] [--provider {nous,openai-codex,spotify}]` | nous, openai-codex, spotify |
| `auth` | `usage: hermes auth [-h] {add,list,remove,reset,status,logout,spotify} ...` | add, list, remove, reset, status, logout, spotify |
| `status` | `usage: hermes status [-h] [--all] [--deep]` | - |
| `cron` | `usage: hermes cron [-h] [--accept-hooks] {list,create,add,edit,pause,resume,run,remove,rm,delete,status,tick} ...` | list, create, add, edit, pause, resume, run, remove, rm, delete, status, tick |
| `webhook` | `usage: hermes webhook [-h] {subscribe,add,list,ls,remove,rm,test} ...` | subscribe, add, list, ls, remove, rm, test |
| `kanban` | `usage: hermes kanban [-h] {init,create,list,ls,show,assign,link,unlink,claim,comment,complete,block,unblock,archive,tail,dispatch,daemon,watch,stats,notify-subscribe,notify-list,notify-unsubscribe,log,runs,heartbeat,assignees,context,gc} ...` | init, create, list, ls, show, assign, link, unlink, claim, comment, complete, block, unblock, archive, tail, dispatch, daemon, watch, stats, notify-subscribe, notify-list, notify-unsubscribe, log, runs, heartbeat, assignees, context, gc |
| `hooks` | `usage: hermes hooks [-h] {list,ls,test,revoke,remove,rm,doctor} ...` | list, ls, test, revoke, remove, rm, doctor |
| `doctor` | `usage: hermes doctor [-h] [--fix]` | - |
| `dump` | `usage: hermes dump [-h] [--show-keys]` | - |
| `debug` | `usage: hermes debug [-h] {share,delete} ...` | share, delete |
| `backup` | `usage: hermes backup [-h] [-o OUTPUT] [-q] [-l LABEL]` | - |
| `import` | `usage: hermes import [-h] [--force] zipfile` | - |
| `config` | `usage: hermes config [-h] {show,edit,set,path,env-path,check,migrate} ...` | show, edit, set, path, env-path, check, migrate |
| `pairing` | `usage: hermes pairing [-h] {list,approve,revoke,clear-pending} ...` | list, approve, revoke, clear-pending |
| `skills` | `usage: hermes skills [-h] {browse,search,install,inspect,list,check,update,audit,uninstall,reset,publish,snapshot,tap,config} ...` | browse, search, install, inspect, list, check, update, audit, uninstall, reset, publish, snapshot, tap, config |
| `plugins` | `usage: hermes plugins [-h] {install,update,remove,rm,uninstall,list,ls,enable,disable} ...` | install, update, remove, rm, uninstall, list, ls, enable, disable |
| `curator` | `usage: hermes curator [-h] {status,run,pause,resume,pin,unpin,restore,backup,rollback} ...` | status, run, pause, resume, pin, unpin, restore, backup, rollback |
| `memory` | `usage: hermes memory [-h] {setup,status,off,reset} ...` | setup, status, off, reset |
| `tools` | `usage: hermes tools [-h] [--summary] {list,disable,enable} ...` | list, disable, enable |
| `mcp` | `usage: hermes mcp [-h] [--accept-hooks] {serve,add,remove,rm,list,ls,test,configure,config,login} ...` | serve, add, remove, rm, list, ls, test, configure, config, login |
| `sessions` | `usage: hermes sessions [-h] {list,export,delete,prune,stats,rename,browse} ...` | list, export, delete, prune, stats, rename, browse |
| `insights` | `usage: hermes insights [-h] [--days DAYS] [--source SOURCE]` | - |
| `claw` | `usage: hermes claw [-h] {migrate,cleanup,clean} ...` | migrate, cleanup, clean |
| `version` | `usage: hermes version [-h]` | - |
| `update` | `usage: hermes update [-h] [--gateway] [--check] [--no-backup] [--backup] [--yes]` | - |
| `uninstall` | `usage: hermes uninstall [-h] [--full] [--yes]` | - |
| `acp` | `usage: hermes acp [-h] [--accept-hooks]` | - |
| `profile` | `usage: hermes profile [-h] {list,use,create,delete,show,alias,rename,export,import} ...` | list, use, create, delete, show, alias, rename, export, import |
| `completion` | `usage: hermes completion [-h] [{bash,zsh,fish}]` | bash, zsh, fish |
| `dashboard` | `usage: hermes dashboard [-h] [--port PORT] [--host HOST] [--no-open] [--insecure] [--tui] [--stop] [--status]` | - |
| `logs` | `usage: hermes logs [-h] [-n LINES] [-f] [--level LEVEL] [--session ID] [--since TIME] [--component NAME] [log_name]` | - |
