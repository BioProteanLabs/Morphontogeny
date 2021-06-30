"""
Helper functions for loading clustering data based on anatomical regions.
"""

import pandas as pd
from numpy import load


def get_best_cluster(structure_acronym:str, clustering_K:int, dr_method:str, filepath:str = "./data"):
    """
    Given a particular brain region and a particular k-value, returns the cluster that best fits that brain region.
    Expects a directory called "data" which contains a file "DICE_scores_master_table.csv" from which to get scores.

    params:
    structure acronym (string): the acronym for the structure you'd like to find the best fit cluster to
    clustering_K (integer): the order of clustering you'd like to find the best fit in.
    dr_method (string): the dimensionality reduction method you'd like to search for clusters in.
    filepath (string): path to the directory containing the master tables and clustering labels.
    """
    assert dr_method in ["DLSC", "PCA"]

    table_filepath = filepath + f"/DICE_scores_master_table_{dr_method}.csv"

    score_frame = pd.read_csv(filepath, index_col=0)

    # filter by region acronym and K value
    # then sort by overlap score, best first
    # then retrieve the top element of the sorted frame

    best_record = score_frame[((score_frame["structure_acronym"] == "".join(['"',structure_acronym,'"'])) & (score_frame['clustering_K'] == clustering_K))].sort_values(by="overlap_score", ascending=False).head(1)

    best_cluster_id = int(best_record.cluster_id) # get the cluster ID

    best_cluster = load(filepath + f"/Kmeans_labels_{dr_method}/{str(clustering_K)}_clusters.npy") == best_cluster_id # load the cluster

    return best_cluster




if __name__ == "__main__":

    cluster = get_best_cluster(structure_acronym="arb", clustering_K=400, dr_method="DLSC")