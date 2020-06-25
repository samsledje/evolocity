from utils import Seq, SeqIO

def load_lee2018(survival_cutoff=0.05):
    pos_map = {}
    with open('data/influenza/escape_lee2018/pos_map.csv') as f:
        f.readline() # Consume header.
        for line in f:
           fields = line.rstrip().split(',')
           pos_map[fields[1]] = int(fields[0]) - 1

    fname = 'data/influenza/escape_lee2018/WSN1933_H1_HA.fa'
    seqs = []
    for record in SeqIO.parse(fname, 'fasta'):
        seq = record.seq
        seqs.append(seq)

    seqs_escape = {}
    antibodies = [
        'C179', 'FI6v3', 'H17L10', 'H17L19', 'H17L7', 'S139',
    ]
    for antibody in antibodies:
        fname = ('data/influenza/escape_lee2018/' +
                 'medianfracsurvivefiles/' +
                 'antibody_{}_median.csv'.format(antibody))
        with open(fname) as f:
            f.readline() # Consume header.
            for line in f:
                fields = line.rstrip().split(',')
                frac_survived = float(fields[3])
                pos = pos_map[fields[0]]
                if seq[pos] != fields[1]:
                    print((seq[pos], fields[1], pos))
                assert(seq[pos] == fields[1])
                escaped = seq[:pos] + fields[2] + seq[pos + 1:]
                assert(len(seq) == len(escaped))
                if escaped not in seqs_escape:
                    seqs_escape[escaped] = []
                seqs_escape[escaped].append({
                    'frac_survived': frac_survived,
                    'antibody': antibody,
                    'significant': frac_survived > survival_cutoff,
                })

    return seq, seqs_escape

def load_lee2019():
    fname = 'data/influenza/escape_lee2019/Perth2009_H3_HA.fa'
    for record in SeqIO.parse(fname, 'fasta'):
        seq = record.seq
        break

    seqs_escape = {}
    fname = 'data/influenza/escape_lee2019/avg_sel_tidy.csv'
    with open(fname) as f:
        f.readline() # Consume header.
        for line in f:
            fields = line.rstrip().split(',')
            significant = fields[14] == 'True'
            pos = int(fields[13])
            assert(seq[pos] == fields[5])
            escaped = seq[:pos] + fields[6] + seq[pos + 1:]
            assert(len(seq) == len(escaped))
            if escaped not in seqs_escape:
                seqs_escape[escaped] = []

            if '-age-' in fields[0]:
                species = 'human'
            elif 'ferret-' in fields[0]:
                species = 'ferret'
            else:
                species = 'antibody'

            seqs_escape[escaped].append({
                'abs_diff_selection': float(fields[11]),
                'antibody': fields[1],
                'species': species,
                'significant': significant,
            })

    return seq, seqs_escape

def load_dingens2017(survival_cutoff=0.9):
    fname = 'data/hiv/escape_dingens2017/BF520c2-Env.fasta'
    record = SeqIO.read(fname, 'fasta')
    seq = Seq.translate(str(record.seq)).rstrip('*')

    seqs_escape = {}
    fname = 'data/hiv/escape_dingens2017/PGT151_1ug_average_mutdiffsel.txt'
    with open(fname) as f:
        f.readline() # Consume header.
        for line in f:
            fields = line.rstrip().split(',')
            pos = int(fields[0]) - 1
            orig, mut = fields[1], fields[2]
            assert(seq[pos] == orig)
            escaped = seq[:pos] + mut + seq[pos + 1:]
            assert(len(seq) == len(escaped))
            diff_sel = float(fields[3])
            if escaped not in seqs_escape:
                seqs_escape[escaped] = []
            seqs_escape[escaped].append({
                'pos': pos,
                'frac_survived': diff_sel,
                'antibody': 'PGT151',
                'significant': diff_sel > survival_cutoff,
            })

    return seq, seqs_escape

def load_dingens2019(survival_cutoff=0.11):
    pos_map = {}
    with open('data/hiv/escape_dingens2019/BG505_to_HXB2.csv') as f:
        f.readline() # Consume header.
        for line in f:
           fields = line.rstrip().split(',')
           pos_map[fields[1]] = int(fields[0]) - 1

    fname = 'data/hiv/escape_dingens2019/Env_protalign_manualeditAD.fasta'
    for record in SeqIO.parse(fname, 'fasta'):
        if record.description == 'BG505':
            seq = record.seq
            break

    seqs_escape = {}
    antibodies = [
        '101074', '10E8', '3BNC117-101074-pool', '3BNC117', 'PG9',
        'PGT121', 'PGT145', 'PGT151', 'VRC01', 'VRC34',
    ]
    for antibody in antibodies:
        fname = ('data/hiv/escape_dingens2019/FileS4/'
                 'fracsurviveaboveavg/{}.csv'.format(antibody))
        with open(fname) as f:
            f.readline() # Consume header.
            for line in f:
                fields = line.rstrip().split(',')
                frac_survived = float(fields[3])
                pos = pos_map[fields[0]]
                assert(seq[pos] == fields[1])
                escaped = seq[:pos] + fields[2] + seq[pos + 1:]
                assert(len(seq) == len(escaped))
                if escaped not in seqs_escape:
                    seqs_escape[escaped] = []
                seqs_escape[escaped].append({
                    'pos': pos,
                    'frac_survived': frac_survived,
                    'antibody': antibody,
                    'significant': frac_survived > survival_cutoff,
                })

    return seq, seqs_escape


if __name__ == '__main__':
    load_dingens2017()
    load_dingens2019()
    load_lee2018()
    load_lee2019()
