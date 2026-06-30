import logging

from flask import Flask

app = Flask(__name__)

TAJ_SVG = '''
<svg viewBox="0 0 800 600" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#fce4c8"/>
      <stop offset="100%" stop-color="#f5e6d3"/>
    </linearGradient>
    <linearGradient id="domeGrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#faf8f5"/>
      <stop offset="100%" stop-color="#e8ddd0"/>
    </linearGradient>
  </defs>

  <rect width="800" height="600" fill="url(#sky)"/>
  <g stroke="#3d2b1f" stroke-linecap="round" stroke-linejoin="round">

    <!-- Reflection Pool -->
    <g stroke-width="1.2" fill="none">
      <rect x="170" y="500" width="460" height="50" rx="3" fill="#e8ddd0" opacity="0.3"/>
      <line x1="185" y1="510" x2="260" y2="510"/>
      <line x1="200" y1="520" x2="340" y2="520"/>
      <line x1="180" y1="530" x2="300" y2="530"/>
      <line x1="320" y1="510" x2="615" y2="510"/>
      <line x1="360" y1="520" x2="600" y2="520"/>
      <line x1="340" y1="530" x2="580" y2="530"/>
      <line x1="450" y1="540" x2="560" y2="540"/>
      <line x1="250" y1="540" x2="380" y2="540"/>
      <line x1="240" y1="545" x2="400" y2="545" stroke-dasharray="4,4"/>
      <line x1="350" y1="545" x2="560" y2="545" stroke-dasharray="4,4"/>
    </g>

    <!-- Walkway / Ground -->
    <line x1="100" y1="555" x2="700" y2="555" stroke-width="2.5"/>
    <g stroke-width="1" stroke-dasharray="3,4" fill="none">
      <line x1="170" y1="565" x2="630" y2="565"/>
      <line x1="170" y1="575" x2="630" y2="575"/>
    </g>

    <!-- Base Platform -->
    <g stroke-width="2.2" fill="url(#domeGrad)">
      <rect x="125" y="440" width="550" height="35"/>
      <rect x="145" y="428" width="510" height="12"/>
      <rect x="108" y="475" width="584" height="12"/>
      <line x1="125" y1="440" x2="675" y2="440" stroke-width="1.5"/>
      <line x1="145" y1="428" x2="655" y2="428" stroke-width="1.5"/>
      <!-- Platform decorative panels -->
      <g stroke-width="1" fill="none">
        <rect x="140" y="448" width="30" height="18" rx="2"/>
        <rect x="630" y="448" width="30" height="18" rx="2"/>
        <rect x="180" y="448" width="30" height="18" rx="2"/>
        <rect x="590" y="448" width="30" height="18" rx="2"/>
      </g>
    </g>

    <!-- Left Minaret -->
    <g stroke-width="2" fill="url(#domeGrad)">
      <rect x="132" y="95" width="24" height="345"/>
      <rect x="128" y="55" width="32" height="12"/>
      <path d="M 128 67 Q 144 80 160 67" fill="none"/>
      <rect x="126" y="155" width="36" height="7"/>
      <rect x="126" y="255" width="36" height="7"/>
      <rect x="126" y="355" width="36" height="7"/>
      <circle cx="144" cy="50" r="6" fill="#faf8f5"/>
      <line x1="144" y1="44" x2="144" y2="32" stroke-width="1.5"/>
      <circle cx="144" cy="29" r="2" fill="#3d2b1f"/>
      <!-- Decorative bands -->
      <line x1="132" y1="105" x2="156" y2="105" stroke-width="1"/>
      <line x1="132" y1="205" x2="156" y2="205" stroke-width="1"/>
      <line x1="132" y1="305" x2="156" y2="305" stroke-width="1"/>
    </g>

    <!-- Right Minaret -->
    <g stroke-width="2" fill="url(#domeGrad)">
      <rect x="644" y="95" width="24" height="345"/>
      <rect x="640" y="55" width="32" height="12"/>
      <path d="M 640 67 Q 656 80 672 67" fill="none"/>
      <rect x="638" y="155" width="36" height="7"/>
      <rect x="638" y="255" width="36" height="7"/>
      <rect x="638" y="355" width="36" height="7"/>
      <circle cx="656" cy="50" r="6" fill="#faf8f5"/>
      <line x1="656" y1="44" x2="656" y2="32" stroke-width="1.5"/>
      <circle cx="656" cy="29" r="2" fill="#3d2b1f"/>
      <line x1="644" y1="105" x2="668" y2="105" stroke-width="1"/>
      <line x1="644" y1="205" x2="668" y2="205" stroke-width="1"/>
      <line x1="644" y1="305" x2="668" y2="305" stroke-width="1"/>
    </g>

    <!-- Side Building Left (Mosque) -->
    <g stroke-width="1.8" fill="url(#domeGrad)">
      <rect x="190" y="365" width="105" height="63"/>
      <rect x="190" y="360" width="105" height="5"/>
      <!-- Arches -->
      <path d="M 200 428 L 200 395 Q 215 380 230 395 L 230 428" fill="none"/>
      <path d="M 235 428 L 235 395 Q 250 380 265 395 L 265 428" fill="none"/>
      <path d="M 270 428 L 270 395 Q 285 380 300 395 L 300 428" fill="none"/>
      <!-- Roof decoration -->
      <line x1="190" y1="360" x2="295" y2="360" stroke-width="2"/>
      <!-- Three small domes -->
      <path d="M 200 360 Q 200 330 215 320 Q 230 330 230 360" fill="#faf8f5"/>
      <path d="M 232 360 Q 232 330 247 320 Q 262 330 262 360" fill="#faf8f5"/>
      <path d="M 264 360 Q 264 330 279 320 Q 294 330 294 360" fill="#faf8f5"/>
      <!-- Finials -->
      <line x1="215" y1="320" x2="215" y2="308" stroke-width="1.2"/>
      <circle cx="215" cy="306" r="2" fill="#3d2b1f"/>
      <line x1="247" y1="320" x2="247" y2="308" stroke-width="1.2"/>
      <circle cx="247" cy="306" r="2" fill="#3d2b1f"/>
      <line x1="279" y1="320" x2="279" y2="308" stroke-width="1.2"/>
      <circle cx="279" cy="306" r="2" fill="#3d2b1f"/>
    </g>

    <!-- Side Building Right (Guest House) -->
    <g stroke-width="1.8" fill="url(#domeGrad)">
      <rect x="505" y="365" width="105" height="63"/>
      <rect x="505" y="360" width="105" height="5"/>
      <path d="M 510 428 L 510 395 Q 525 380 540 395 L 540 428" fill="none"/>
      <path d="M 545 428 L 545 395 Q 560 380 575 395 L 575 428" fill="none"/>
      <path d="M 580 428 L 580 395 Q 595 380 600 395 L 600 428" fill="none"/>
      <line x1="505" y1="360" x2="610" y2="360" stroke-width="2"/>
      <path d="M 510 360 Q 510 330 525 320 Q 540 330 540 360" fill="#faf8f5"/>
      <path d="M 545 360 Q 545 330 560 320 Q 575 330 575 360" fill="#faf8f5"/>
      <path d="M 580 360 Q 580 330 595 320 Q 610 330 610 360" fill="#faf8f5"/>
      <line x1="525" y1="320" x2="525" y2="308" stroke-width="1.2"/>
      <circle cx="525" cy="306" r="2" fill="#3d2b1f"/>
      <line x1="560" y1="320" x2="560" y2="308" stroke-width="1.2"/>
      <circle cx="560" cy="306" r="2" fill="#3d2b1f"/>
      <line x1="595" y1="320" x2="595" y2="308" stroke-width="1.2"/>
      <circle cx="595" cy="306" r="2" fill="#3d2b1f"/>
    </g>

    <!-- Main Building Body -->
    <g stroke-width="2" fill="url(#domeGrad)">
      <!-- Main block -->
      <rect x="270" y="280" width="260" height="148"/>
      <!-- Chamfered corners -->
      <line x1="270" y1="280" x2="255" y2="295" stroke-width="1.5"/>
      <line x1="530" y1="280" x2="545" y2="295" stroke-width="1.5"/>
      <line x1="255" y1="295" x2="255" y2="428" stroke-width="1.5"/>
      <line x1="545" y1="295" x2="545" y2="428" stroke-width="1.5"/>
      <!-- Top cornice -->
      <rect x="255" y="275" width="290" height="8"/>
      <path d="M 255 283 L 270 290 L 530 290 L 545 283" fill="none"/>
      <!-- Decorative line -->
      <line x1="270" y1="310" x2="530" y2="310" stroke-width="1.2"/>
      <line x1="270" y1="395" x2="530" y2="395" stroke-width="1.2"/>

      <!-- Main Iwan (Great Arch) -->
      <path d="M 335 428 L 335 370 Q 400 340 465 370 L 465 428" fill="#f5e6d3" stroke-width="2.5"/>
      <path d="M 345 428 L 345 375 Q 400 350 455 375 L 455 428" fill="#e8ddd0" stroke-width="1.2"/>
      <line x1="400" y1="348" x2="400" y2="338" stroke-width="1.5"/>
      <circle cx="400" cy="335" r="4" fill="#3d2b1f"/>

      <!-- Side arches left -->
      <path d="M 275 428 L 275 390 Q 295 370 315 390 L 315 428" fill="#f5e6d3" stroke-width="1.5"/>
      <path d="M 280 428 L 280 393 Q 295 378 310 393 L 310 428" fill="#e8ddd0" stroke-width="1"/>

      <!-- Side arches right -->
      <path d="M 485 428 L 485 390 Q 505 370 525 390 L 525 428" fill="#f5e6d3" stroke-width="1.5"/>
      <path d="M 490 428 L 490 393 Q 505 378 520 393 L 520 428" fill="#e8ddd0" stroke-width="1"/>

      <!-- Small arches row -->
      <g stroke-width="1" fill="#f5e6d3">
        <path d="M 275 310 L 275 330 Q 290 340 305 330 L 305 310"/>
        <path d="M 315 310 L 315 330 Q 330 340 345 330 L 345 310"/>
        <path d="M 455 310 L 455 330 Q 470 340 485 330 L 485 310"/>
        <path d="M 495 310 L 495 330 Q 510 340 525 330 L 525 310"/>
      </g>
    </g>

    <!-- Main Dome -->
    <g stroke-width="2.5" fill="#faf8f5">
      <!-- Dome drum (cylindrical base) -->
      <rect x="305" y="258" width="190" height="20"/>
      <line x1="305" y1="268" x2="495" y2="268" stroke-width="1"/>
      
      <!-- Main onion dome -->
      <path d="M 290 280 
               C 290 220, 310 140, 400 80 
               C 490 140, 510 220, 510 280" />
      
      <!-- Dome outline double line detail -->
      <path d="M 300 280 
               C 300 225, 318 150, 400 95 
               C 482 150, 500 225, 500 280" 
            stroke-width="1" stroke="#d4c5a9"/>
      
      <!-- Dome base decorative band -->
      <path d="M 293 275 Q 400 290 507 275" fill="none" stroke-width="1.5"/>
    </g>

    <!-- Main Dome Finial -->
    <g stroke-width="1.8">
      <line x1="400" y1="80" x2="400" y2="55"/>
      <circle cx="400" cy="50" r="5" fill="#faf8f5"/>
      <line x1="395" y1="45" x2="405" y2="45" stroke-width="1"/>
      <path d="M 398 55 L 395 48 M 402 55 L 405 48" stroke-width="1"/>
    </g>

    <!-- Side Domes (Chatris) -->
    <g stroke-width="1.8" fill="#faf8f5">
      <!-- Left chatri -->
      <rect x="258" y="260" width="30" height="18"/>
      <path d="M 255 280 Q 255 230 273 215 Q 291 230 291 280"/>
      <line x1="273" y1="215" x2="273" y2="203" stroke-width="1.2"/>
      <circle cx="273" cy="200" r="2.5" fill="#3d2b1f"/>

      <!-- Right chatri -->
      <rect x="512" y="260" width="30" height="18"/>
      <path d="M 509 280 Q 509 230 527 215 Q 545 230 545 280"/>
      <line x1="527" y1="215" x2="527" y2="203" stroke-width="1.2"/>
      <circle cx="527" cy="200" r="2.5" fill="#3d2b1f"/>
    </g>

    <!-- Birds in Sky -->
    <g stroke-width="1" fill="none">
      <path d="M 150 80 Q 155 75 160 80 Q 165 75 170 80"/>
      <path d="M 620 60 Q 627 55 634 60 Q 641 55 648 60"/>
      <path d="M 670 90 Q 675 86 680 90 Q 685 86 690 90"/>
      <path d="M 130 110 Q 136 105 142 110 Q 148 105 154 110"/>
      <path d="M 590 120 Q 594 116 598 120 Q 602 116 606 120"/>
    </g>

    <!-- Clouds -->
    <g stroke-width="0.8" fill="none" opacity="0.4">
      <path d="M 100 50 Q 120 40 140 50 Q 160 45 180 55 Q 160 60 140 58 Q 120 62 100 50"/>
      <path d="M 620 30 Q 640 20 660 30 Q 680 25 700 35 Q 680 40 660 38 Q 640 42 620 30"/>
    </g>

  </g>
</svg>
'''

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Taj Mahal Sketch</title>
  <style>
    * {{ margin: 0; padding: 0; }}
    body {{
      min-height: 100vh;
      background: #1a1a2e;
      display: flex;
      justify-content: center;
      align-items: center;
      font-family: 'Georgia', serif;
    }}
    .card {{
      background: #faf6f0;
      border-radius: 12px;
      padding: 30px 40px 20px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.5);
      text-align: center;
    }}
    h1 {{
      color: #8b6914;
      font-weight: 400;
      letter-spacing: 6px;
      font-size: 20px;
      text-transform: uppercase;
      margin-bottom: 15px;
      border-bottom: 1px solid #d4c5a9;
      padding-bottom: 10px;
    }}
    svg {{
      max-width: 100%;
      height: auto;
      display: block;
    }}
    .caption {{
      margin-top: 12px;
      color: #8b7355;
      font-size: 12px;
      letter-spacing: 2px;
      font-style: italic;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>&#x2726; Taj Mahal &#x2726;</h1>
    {svg}
    <p class="caption">&#x2014; A Sketch &#x2014;</p>
  </div>
</body>
</html>
'''


@app.route('/')
def taj_mahal():
    '''Return a Taj Mahal sketch page.'''
    return HTML_TEMPLATE.format(svg=TAJ_SVG)


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return '''
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    '''.format(e), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
