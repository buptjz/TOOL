#http://blog.csdn.net/cserchen/article/details/7535182
'''
在广告中，根据CTR预测的高低，将最有可能被用户点击的广告按顺序依次展现，
根据点击反馈，可以生成ROC曲线（y方向，点击+1；x方向，未点击+1），
很明显，用户点击的越多，被点击的广告排序越靠前，ROC曲线下的面积越大，
即AUC越大，则表明广告投放的效果越好，也就是CTR预测越准确
'''
def scoreClickAUC(num_clicks, num_impressions, predicted_ctr):
    """
    Calculates the area under the ROC curve (AUC) for click rates
    
    Parameters
    ----------
    num_clicks : a list containing the number of clicks

    num_impressions : a list containing the number of impressions
    impression应该指的是曝光

    predicted_ctr : a list containing the predicted click-through rates

    Returns
    -------
    auc : the area under the ROC curve (AUC) for click rates
    """
    #从ctr大到小排序
    i_sorted = sorted(range(len(predicted_ctr)),key=lambda i: predicted_ctr[i],
                      reverse=True)
    auc_temp = 0.0
    click_sum = 0.0
    old_click_sum = 0.0
    no_click = 0.0
    no_click_sum = 0.0

    # treat all instances with the same predicted_ctr as coming from the
    # same bucket
    last_ctr = predicted_ctr[i_sorted[0]] + 1.0

    for i in range(len(predicted_ctr)):
        if last_ctr != predicted_ctr[i_sorted[i]]:
            auc_temp += (click_sum+old_click_sum) * no_click / 2.0#求梯形面积
            old_click_sum = click_sum#let the old to be the current one
            no_click = 0.0
            last_ctr = predicted_ctr[i_sorted[i]]
        no_click += num_impressions[i_sorted[i]] - num_clicks[i_sorted[i]]#non-click = pv - click
        no_click_sum += num_impressions[i_sorted[i]] - num_clicks[i_sorted[i]]
        click_sum += num_clicks[i_sorted[i]]
    auc_temp += (click_sum+old_click_sum) * no_click / 2.0
    auc = auc_temp / (click_sum * no_click_sum)#归一化
    return

def main():
    import sys
    if len(sys.argv) != 3:
        print("Usage: python scoreKDD.py solution_file.csv submission_file.csv")
        sys.exit(2)

    num_clicks, num_impressions = read_solution_file(sys.argv[1])
    predicted_ctr = read_submission_file(sys.argv[2])

    auc = scoreClickAUC(num_clicks, num_impressions, predicted_ctr)
    print("AUC  : %f" % auc)
