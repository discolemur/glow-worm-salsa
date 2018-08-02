#! /usr/bin/env python3.5

ACOL = '#ff0000'
TCOL = '#0000ff'
CCOL = '#00ff00'
GCOL = '#ffff00'
DEFCOL = '#ff0000'

def readSeqs(filename) :
  ifh = open(filename, 'rt')
  lines = ifh.readlines()
  seqs = {}
  h = ''
  for i in range(len(lines)) :
    if i % 2 :
      seqs[h] = lines[i].strip().upper()
    else :
      h = lines[i].strip()
  ifh.close()
  return seqs , sorted([ l.strip() for l in lines[::2] ])

def readScores(filename) :
  ifh = open(filename, 'rt')
  lines = ifh.readlines()
  scores = {}
  h = ''
  for i in range(len(lines)) :
    if i % 2 :
      scores[h] = [ ord(S) - 97 for S in lines[i].strip() ]
    else :
      h = lines[i].strip()
  ifh.close()
  maxScore = max( [ max(scores[h]) for h in scores ] )
  minScore = min( [ min(scores[h]) for h in scores ] )
  return scores , minScore , maxScore

def scoreToColor(minScore, maxScore, score, _col) :
  normalized = int((255 / (maxScore - minScore)) * score - ((minScore * 255)/(maxScore - minScore)))
  alpha = hex( normalized )[-2:] if normalized > 0 else '00'
  return '%s%s' %(_col , alpha)

def seqToHtml(seq, scoresSeq, header, MIN_SCORE, MAX_SCORE, monochromatic) :
  global ACOL
  global TCOL
  global CCOL
  global GCOL
  global DEFCOL
  size = '0.9rem'
  xhtml = '<tr><td>%s</td><td>' %header
  for i in range(len(seq)) :
    char = seq[i]
    score = scoresSeq[i]
    color = DEFCOL
    if char == 'A' and not monochromatic :
      color = scoreToColor(MIN_SCORE, MAX_SCORE, score, ACOL)
    elif char == 'T' and not monochromatic :
      color = scoreToColor(MIN_SCORE, MAX_SCORE, score, TCOL)
    elif char == 'C' and not monochromatic :
      color = scoreToColor(MIN_SCORE, MAX_SCORE, score, CCOL)
    elif char == 'G' and not monochromatic :
      color = scoreToColor(MIN_SCORE, MAX_SCORE, score, GCOL)
    xhtml = xhtml + '<span style=\'line-height: %s; text-align: center; height: %s; width: %s; display: inline-block; font-size: %s; background: %s;\'>%s</span>' %(size, size, size, size, color, char)
  xhtml = xhtml + '</td></tr>'
  return xhtml

def _getScaleOneColor(minScore, maxScore, _col) :
  _colMin = scoreToColor(minScore, maxScore, minScore, _col)
  _colMax = scoreToColor(minScore, maxScore, maxScore, _col)
  return '<div style=\'display: block; height: 1rem; padding-left: 0.5rem; margin-top: 0.2rem;\'><span>%d</span><div style=\'margin-left: 0.2rem; margin-right: 0.2rem; border: solid #000000 1px; background: linear-gradient(to right, %s, %s); display: inline-block; height: 0.5rem; width: 5rem;\'></div><span>%d</span></div>' %(minScore, _colMin, _colMax, maxScore)

# report the color scale at the bottom. 0 [clear (linear-gradient) opaque] ${maximum p-value}
def getScale(minScore, maxScore, monochromatic) :
  global ACOL
  global TCOL
  global CCOL
  global GCOL
  global DEFCOL
  _col = DEFCOL
  xhtml = '<div style=\'display: block; height: 1rem; padding-top: 0.5rem; font-size: 0.6rem;\'><span>Min -log10(p-value)</span><div style=\'margin-left: 0.2rem; margin-right: 0.2rem; background: none; display: inline-block; height: 0.5rem; width: 1rem;\'></div><span>Max -log10(p-value)</span></div>'
  if monochromatic :
    xhtml = xhtml + _getScaleOneColor(minScore, maxScore, _col)
  else :
    xhtml = xhtml + _getScaleOneColor(minScore, maxScore, ACOL)
    xhtml = xhtml + _getScaleOneColor(minScore, maxScore, TCOL)
    xhtml = xhtml + _getScaleOneColor(minScore, maxScore, CCOL)
    xhtml = xhtml + _getScaleOneColor(minScore, maxScore, GCOL)
  return xhtml

def main(filestub, monochromatic) :
  seqs , headers = readSeqs('%s.overlaps' %filestub)
  scores , minScore , maxScore = readScores('%s.scores' %filestub)
  title = filestub.replace('important', 'Assembled from ').replace('.txt', '-mers')
  xhtml = '<html><span>%s</span><table style=\'width: 100%%; display: block;\'>' %title
  for h in headers :
    xhtml = xhtml + seqToHtml(seqs[h], scores[h], h, minScore, maxScore, monochromatic)
  xhtml = xhtml + '</table>' + getScale(minScore, maxScore, monochromatic) + '</html>'
  ofh = open('%s.html' %filestub, 'wt')
  ofh.write(xhtml)
  ofh.close()

if __name__ == '__main__' :
  from argparse import ArgumentParser
  parser = ArgumentParser()
  parser.add_argument('filestub', help='filestub.overlaps and filestub.scores')
  parser.add_argument('-m', default=False, action='store_true', help='monochromatic')
  args = parser.parse_args()
  main(args.filestub, args.m)
