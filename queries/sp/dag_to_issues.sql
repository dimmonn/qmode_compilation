SELECT i.id                                             AS issue_id,
       i.created_at,
       i.closed_at,
       TIMESTAMPDIFF(MINUTE, i.created_at, i.closed_at) AS issue_resolution_time,
       c.in_degree,
       c.out_degree,
       c.average_degree,
       merge_count,
       is_merge,
       CASE
           WHEN RAND() <= 0.8 THEN 'train'
           ELSE 'validation'
           END                                          AS dataset_split

FROM project_issue i
         JOIN
     project_issue_bug_introducing_commits bibc ON i.id = bibc.project_issue_id
         JOIN
     commit c ON bibc.bug_introducing_commits_sha = c.sha;