API Design
Discord Integration
DM Discord Bot -> !verify
- Provide private key of holder wallet
- Discord bot signs transaction & verifies NFT is in wallet
- Discord bot gives you verified role in discord
- Discord bot gives you Key for bot input
- Discord bot creates database entry within API
- Provides:
- Discord dev ID
- key generated
- empty session id
- mint address of token owned

Api for above done - Need to update auth_token status

DM Discord Bot -> !reset
- Discord bot searches API with your discord ID
If Found:
-> Resets session ID so that you can re-launch bot
If Not Found:
-> Prompts you to !verify as you’re not in API

DM Discord Bot -> !info
-Discord bot searches API with your discord ID
If Found:
-> Sends all info back
If Not Found
-> Prompts you to !verify as you’re not in API

DM Discord Bot -> !key
-Discord bot searches API with your discord ID
If Found:
-> Generates & Sends new key
-> Updates current key in API to new key
If Not Found:
-> Prompts you to !verify as you’re not in the API

Script monitors all NFT’s and checks for a change of owner
- On owner change
- Sends request to API to delete account associated with mint address
- Removes Role from discord ID associated with mint address

On Bot open -> Pings API with bot key
-> Checks session id and compares to current session
-> if different prompts to !reset with Discord Bot. Bot auth is not passed
-> if session is same then bot auth is passed
-> if session is empty then adds session to API and bot auth is passed
