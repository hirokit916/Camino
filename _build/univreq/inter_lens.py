# Manual classification: does an English-medium international school IN JAPAN exempt a Japanese student from the English test?
# A = yes, inter-school years count (value = years needed; 0 = no number stated)
# B = school years don't count, but test scores (SAT/ACT, IB/AP/A Level English) can exempt
# C = no route for an inter student in Japan (English-speaking-country schooling/nationality only)
# D = no exemption for non-native speakers at all
# E = English test not required, or only recommended
# U = not confirmed on official page
L = {
 'MIT':('E',5),'Princeton University':('A',3),'Harvard University':('E',0),'Yale University':('A',2),'California Institute of Technology':('A',0),
 'Stanford University':('E',0),'University of Pennsylvania':('A',3),'Duke University':('E',0),'Johns Hopkins University':('E',3),'Northwestern University':('A',0),
 'University of Chicago':('U',0),'Columbia University':('A',0),'Dartmouth College':('A',2),'Carnegie Mellon University':('D',0),'Cornell University':('A',4),
 'Brown University':('E',0),'Rice University':('A',2),'Vanderbilt University':('B',0),'Washington University in St. Louis':('A',3),
 'University of California, Berkeley':('A',0),'University of California, Los Angeles':('A',0),'University of Notre Dame':('B',0),
 'Emory University':('A',4),'Georgetown University':('E',0),'University of Michigan–Ann Arbor':('C',0),'University of Virginia':('E',0),
 'University of North Carolina at Chapel Hill':('D',0),'University of Southern California':('B',0),'Georgia Institute of Technology':('U',0),
 'University of California, San Diego':('A',0),
 'Boston College':('B',0),'New York University':('A',3),'Tufts University':('A',3),'Boston University':('U',0),'University of California, Davis':('A',0),
 'University of California, Irvine':('A',0),'University of Florida':('U',0),'University of Illinois Urbana-Champaign':('C',0),'University of Texas at Austin':('C',0),
 'University of Wisconsin–Madison':('A',4),'Wake Forest University':('A',3),'Northeastern University':('C',0),'Villanova University':('A',3),
 'Case Western Reserve University':('A',2),'Lehigh University':('A',2),'Ohio State University':('C',0),'Rutgers University–New Brunswick':('U',0),
 'University of California, Santa Barbara':('A',0),'University of Maryland, College Park':('C',0),'University of Rochester':('A',3),'University of Washington':('C',0),
 'University of Georgia':('U',0),'Virginia Tech':('C',0),'William & Mary':('E',4),'Pennsylvania State University':('C',0),'Purdue University':('U',0),
 'Santa Clara University':('A',4),'University of Miami':('B',0),'Brandeis University':('A',4),'Florida State University':('D',0),'George Washington University':('A',4),
 'Stevens Institute of Technology':('C',0),'Stony Brook University (SUNY)':('A',0),'Texas A&M University':('C',0),'Tulane University':('B',0),
 'University of Massachusetts Amherst':('U',0),'University of Minnesota Twin Cities':('B',0),'University of Pittsburgh':('B',0),'Michigan State University':('C',0),
 'Rensselaer Polytechnic Institute':('B',0),'University of California, Merced':('A',0),'Syracuse University':('C',0),'Binghamton University (SUNY)':('A',4),
 'Howard University':('A',0),'Indiana University Bloomington':('B',0),'North Carolina State University':('C',0),'Rutgers University–Newark':('U',0),
 'University of Connecticut':('B',0),'Worcester Polytechnic Institute':('C',0),'Clemson University':('C',0),'Colorado School of Mines':('C',0),
 'Drexel University':('A',3),'Pepperdine University':('A',4),'University of California, Riverside':('A',0),'Fordham University':('D',0),
 'New Jersey Institute of Technology':('C',0),'Southern Methodist University':('A',0),'University at Buffalo (SUNY)':('C',0),'University of Delaware':('D',0),
 'Baylor University':('A',1),'Gonzaga University':('C',0),'Marquette University':('C',0),'Texas Christian University':('U',0),'Yeshiva University':('A',0),
 'American University':('A',4),'Rochester Institute of Technology':('C',0),'Rutgers University–Camden':('B',0),'University of Illinois Chicago':('B',0),
 'University of Missouri':('C',0),'Auburn University':('C',0),'Chapman University':('A',0),'Creighton University':('A',0),'Elon University':('A',0),
 'Florida International University':('U',0),'Saint Louis University':('A',0),'University of Iowa':('C',0),'University of San Diego':('U',0),
 'University of South Florida':('B',0),
}
if __name__=='__main__':
    import sys; sys.path.insert(0,'.')
    import us_data, us_data2
    US=us_data.US+us_data2.US3
    miss=[d['en'] for d in US if d['en'] not in L]; print('missing',miss, len(L), len(US))
    def band(r): return '1-30' if r<=30 else '31-50' if r<=50 else '51-100'
    from collections import Counter
    for b in ['1-30','31-50','51-100']:
        c=Counter(L[d['en']][0] for d in US if band(d['rank'])==b); print(b, sum(c.values()), dict(sorted(c.items())))
    c=Counter(L[d['en']][0] for d in US); print('all',dict(sorted(c.items())))
    yrs=Counter(L[d['en']][1] for d in US if L[d['en']][0]=='A'); print('A years',dict(sorted(yrs.items())))
    print('4yr+', [d['en'] for d in US if L[d['en']][0] in 'AE' and L[d['en']][1]>=4])
PUBLIC = set('''University of California, Berkeley|University of California, Los Angeles|University of California, San Diego|University of California, Davis|University of California, Irvine|University of California, Santa Barbara|University of California, Merced|University of California, Riverside|University of Michigan–Ann Arbor|University of Virginia|University of North Carolina at Chapel Hill|Georgia Institute of Technology|University of Florida|University of Illinois Urbana-Champaign|University of Texas at Austin|University of Wisconsin–Madison|Ohio State University|Rutgers University–New Brunswick|University of Maryland, College Park|University of Washington|University of Georgia|Virginia Tech|William & Mary|Pennsylvania State University|Purdue University|Florida State University|Stony Brook University (SUNY)|Texas A&M University|University of Massachusetts Amherst|University of Minnesota Twin Cities|University of Pittsburgh|Michigan State University|Binghamton University (SUNY)|Indiana University Bloomington|North Carolina State University|Rutgers University–Newark|University of Connecticut|Clemson University|Colorado School of Mines|New Jersey Institute of Technology|University at Buffalo (SUNY)|University of Delaware|University of Illinois Chicago|University of Missouri|Rutgers University–Camden|Auburn University|Florida International University|University of Iowa|University of South Florida'''.split('|'))
