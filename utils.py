def naming_file(info):
    if (info['nde'] == 'ir') | (info['nde'] == 'ae'):
        return '{}_{}_{}_{}.csv'.format(info['nde'], info['exp_id'], 
                                        info['loading_amp'].replace('.','-'), info['percent_fatigue_life'])

    elif info['nde'] == 'lu':
        return '{}_{}_{}_{}_{}.csv'.format(info['nde'], info['exp_id'], 
                                            info['loading_amp'].replace('.','-'), info['percent_fatigue_life'],
                                            info['position'])

    elif info['nde'] == 'nlu':
        return '{}_{}_{}_{}_{}_{}.csv'.format(info['nde'], info['exp_id'], 
                                            info['loading_amp'].replace('.','-'), info['percent_fatigue_life'],
                                            info['position'], info['nlu_amp'])