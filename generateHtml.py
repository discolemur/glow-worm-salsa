#! /usr/bin/env python3.5

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
  return seqs , [ l.strip() for l in lines[::2] ]

def seqToHtml(seq, scoresSeq, header, monochromatic) :
  scoresSeq = [ ord(S) - 97 for S in scoresSeq ]
  MAX = max(scoresSeq)
  size = '0.9rem'
  xhtml = '<tr><td>%s</td><td>' %header
  for i in range(len(seq)) :
    char = seq[i]
    score = hex( int(scoresSeq[i] * 255  / MAX) )[-2:]
    alpha = '%s' %score
    color = '#ff0000'
    if char == 'A' and not monochromatic :
      color = '#ff0000'
    elif char == 'T' and not monochromatic :
      color = '#0000ff'
    elif char == 'C' and not monochromatic :
      color = '#00ff00'
    elif char == 'G' and not monochromatic :
      color = '#ffff00'
    color = color + alpha
    xhtml = xhtml + '<span style=\'line-height: %s; text-align: center; height: %s; width: %s; display: inline-block; font-size: %s; background: %s;\'>%s</span>' %(size, size, size, size, color, char)
  xhtml = xhtml + '</td></tr>'
  return xhtml

def main(filestub, monochromatic) :
  seqs , headers = readSeqs('%s.overlaps' %filestub)
  scores , _h = readSeqs('%s.scores' %filestub)
  xhtml = '<html><table>'
  for h in headers :
    xhtml = xhtml + seqToHtml(seqs[h], scores[h], h, monochromatic)
  xhtml = xhtml + '</table></html>'
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
