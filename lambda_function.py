def lambda_handler(event, context):
  import base64
  import json
  import io
  import urllib.parse
  from PIL import Image, ImageDraw, ImageFont

  #print(json.dumps(event))
  
  if event['pathParameters']: # this will be "null" if the root of the app is requested
    print(event['pathParameters']['proxy'])
    input = '/' + urllib.parse.unquote(event['pathParameters']['proxy']) # path will now be preceded by "darth" so bodge in this check
  else:
    print('/')
    input = '/'
  
  if input == '/':
    message = 'and\ndead\nmen.'
  else:
    msg_split = input.split('/')[1:]
    if len(msg_split) == 1:
      message = 'and\n' + msg_split[0][:8] + '.'
    elif len(msg_split) >= 2:
      message = 'and\n' + msg_split[0][:8] + '\n' + msg_split[1][:7] + '.'
  
  image = Image.open('images/darth_background.png')

  draw = ImageDraw.Draw(image)
  
  font = ImageFont.truetype('fonts/komika_kaps.ttf', size=17)
  
  color = 'rgb(0, 0, 0)'
  
  (x, y) = (205, 25)
  basemessage = 'all i am\nsurrounded\nby is fear.'
  draw.multiline_text((x, y), basemessage, fill=color, font=font, align='center', spacing=-5)
   
  (x, y) = (315, 88)
  
  w, h = draw.textsize(message, font=font)
  draw.multiline_text((x-(w/2), y-(h/2)), message, fill=color, font=font, align='center', spacing=-5)

  buffered = io.BytesIO()
  image.save(buffered, format="PNG")
  img_str = base64.b64encode(buffered.getvalue()).decode('ascii')

  return {
    'statusCode': 200,
  	'headers': {'Content-type': 'image/png'},
  	'isBase64Encoded': True,
    'body': img_str
  }
