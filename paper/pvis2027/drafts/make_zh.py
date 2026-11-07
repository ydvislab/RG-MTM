"""Build the Chinese manuscript: fill the tabular bodies of the English tables into
method_anchor_figures_updated_zh.src.tex with Chinese captions and notes."""
import re
from pathlib import Path
D = Path(__file__).resolve().parent
P = D.parent

def tabular(path, wide=False):
    s = (P / path).read_text()
    m = re.search(r'\\begin\{tabular\*?\}.*?\\end\{tabular\*?\}', s, re.S)
    t = m.group(0)
    t = re.sub(r'\\begin\{tabular\*\}\{\\(?:textwidth|columnwidth)\}\{@\{\\extracolsep\{\\fill\}\}', r'\\begin{tabular}{@{}', t)
    t = t.replace('\\end{tabular*}', '\\end{tabular}')
    t = t.replace('& Mode &', '& 模式 &')
    return ('\\resizebox{\\textwidth}{!}{' + t + '}') if wide else t

def table(label, cap, body, note, star=False):
    return ('\\begin{table}[htbp]\n\\centering\n\\caption{' + cap + '}\\label{' + label + '}\n'
            '\\footnotesize\\setlength{\\tabcolsep}{3pt}\n' + body + '\n\\par\\smallskip\n'
            '\\parbox{\\linewidth}{\\footnotesize ' + note + '}\n\\end{table}')

T = {
'%%TABLE_PARAMS%%': table('tab:anchor-parameters-final', 'Balanced 模式的参数设置与运行时间（秒）。',
    tabular('section5_revision_20261105/table2_parameters_runtime.tex'),
    '权重 $(4,1,0.5,0.1)$ 和 $\\rho=0.5$ 固定。$s_w$ 为单位支撑测度对应的宽度；$L$ 为栅格长度。时间为在 Apple M4 上的一次运行，分别为优化时间和完整流程时间。'),
'%%TABLE_COMPARISON%%': table('tab:quantitative-final', '四个数据集的比较。粗体/下划线标出每个数据集中本地测量值的最好/次好（取不同的值）；并列者共享标记。曲线使用固定的默认方向。',
    tabular('section5_revision_20261105/table1_comparison.tex', wide=True),
    '$^\\dagger$灰色：已发表的 TMTM/ST-MTM Temporal 的 SNS/TW（ST-MTM 论文表 1，作者的输入），仅供参考，不参与标记；其余均为同一输入上的本地测量。作者的输入和覆盖未经确认。本地 TW 覆盖（Gaussian/Ring/Wildfires/Storms）为 64/64、1/40、4/32、11/744；不合格的帧省略。已发表的 TW 只有两位小数。“模式”只适用于 AnchorMTM。'),
'%%TABLE_VOLPARAMS%%': table('tab:volume-parameters', '体数据集与 Balanced 模式的参数设置。',
    tabular('volume_comparison_final_20261106/table_volume_parameters.tex'),
    '权重依次为参考、几何、时间和偏心。$s_w$ 为单位支撑测度对应的宽度（Cylinder 为体素数；Tangaroa 为物理体积）；$L$ 为栅格长度，不同于物理画布长度 $L_{world}$。Exact 的允许量为零，其他参数与对应的 Balanced 相同。'),
'%%TABLE_VOLUME%%': table('tab:volume-comparison', '固定 $x$ 参考下的体数据比较。粗体/下划线标出每个数据集的最好/次好（取不同的值）；并列者共享标记。',
    tabular('volume_comparison_final_20261106/table_volume.tex'),
    '所有值均为本地测量，包括适配后的 TMTM。TW 取 $k=1$，覆盖 102/102 和 201/201。“模式”只适用于 AnchorMTM。配置是冻结的探索性结果，不是盲测；设置见表~\\ref{tab:volume-parameters}。'),
}
src = (D / 'method_anchor_figures_updated_zh.src.tex').read_text()
for k, v in T.items():
    assert src.count(k) == 1, k
    src = src.replace(k, v)
src = src.replace('% 由 make_zh.py 从本文件生成', '% 由 make_zh.py 从 method_anchor_figures_updated_zh.src.tex 生成，请改 .src.tex 后重新生成')
(D / 'method_anchor_figures_updated_zh.tex').write_text(src)
print('written')
