with sq_views as (
    select
        e.item_luid,
        e.item_name,
        e.view_workbook_name,
        e.item_parent_project_name,
        e.owner_email,
        e.item_hyperlink,
        e.first_published_at,
        e.last_access_date
    from
        adm_sitecontent e
    where
        e.item_type = 'View'
        and item_parent_project_name = 'SonarQube'
        and item_luid is not null
),
sq_events as (
    select
        project_name,
        event_name,
        item_luid,
        item_name,
        event_date,
        julianday('now') - julianday(event_date) as days_since_last_access,
        actor_user_name,
        row_number() over (
            partition by item_luid,
            actor_user_name
            order by
                event_date desc
        ) as rno,
        row_number() over (
            partition by item_luid
            order by
                event_date desc
        ) as access_no
    from
        adm_tsevents
    where
        project_name = 'SonarQube'
        and event_name = 'Access View'
        and item_luid is not null
),
last_event as (
    select
        *
    from
        sq_events
    where
        access_no = 1
)
select
    v.item_luid,
    v.item_parent_project_name,
    v.item_name,
    v.view_workbook_name,
    v.last_access_date,
    e.event_date,
    e.days_since_last_access,
    e.actor_user_name,
    v.owner_email,
    v.item_hyperlink,
    v.first_published_at
from
    last_event e
    inner join sq_views v using(item_luid)
order by
    days_since_last_access desc