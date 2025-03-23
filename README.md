<div align="center">
  <a href="mailto:marechan@mc.theserver.life" style="display: block; text-align: center;">
    <img
      alt="Image of this repo"
      src="https://togp.xyz?owner=douxxtech&repo=marechan&bash-dark-all&cache=false"
      type="image/svg+xml"
      style="border-radius: 20px; overflow: hidden;"
    />
    <h1 align="center">MareChan - My Assistant Reading Emails</h1>
  </a>
    <p align="center">Marechan is a 100% selfhosted AI that replies to your mails</p>
</div>


# Chat with Marechan !
To directly try marechan, send an email to [marechan@mc.theserver.life](mailto:marechan@mc.theserver.life)

## 1. How to setup

1. To setup marechan, first clone this repository.
```
git clone https://github.com/douxxtech/marechan
```
2. Navigate to the cloned project and then install the requirements. Make sure you have python3 and pip3 installed.
```
cd marechan
pip3 install -r requirements.txt
```

3. Edit the configuration file and the assistant file
- config.conf: You can here edit some specific things, and setup the logs via discord webhook

- assistants.json: here you can edit all your assistants, with their prompts. Prompt enhancments are provided by [utils/prompt_enhancer.py](utils/prompt_enhancer.py)

4. Make the marechan file executable:
On linux:
```
chmod +x marechan.py
```

5. Transport the mail to marechan, the mail imput should go in the STDIN of the file.
> It depends on the mail server you are using, so no specific tutorial here.

## 2. Need help ?
Configurating can be a bit hard, so please open an issue if you need any help.

## LICENSE
Licensed under GPL-3.0