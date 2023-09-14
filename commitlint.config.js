module.exports = {
    rules: {
        'subject-min-length': [2, 'always', 10],
        'subject-max-length': [2, 'always', 80],
        'subject-case': [2, 'always', 'sentence-case'],
        'subject-full-stop': [2, 'never', '.'],
        'body-min-length': [2, 'always', 0],
        'body-max-line-length': [2, 'always', 100],
        'body-case': [2, 'always', 'sentence-case'],
        'body-full-stop': [2, 'always', '.'],
        'footer-min-length': [2, 'always', 0],
        'footer-max-line-length': [2, 'always', 100],
        'type-enum': [2, 'always', [
            'breaking', 'deps', 'chore', 'ci', 'docs', 'feat', 'fix', 'perf', 'refactor', 'style', 'test'
         ]],
         'type-empty': [2, 'never']
    },
    parserPreset: './commitlint.parser-preset.js',
    defaultIgnores: false
};
