CREATE_EMPLOYEE="""
CREATE(e:employees {
    Edescription: $Edescription,
    Ephone: $Ephone,
    EName: $Ename,
    Eid: $Eid,
    password: $Epassword,
    Egender: $Egender,
    Efile_path: $Efile_path,
    Ebirth_date: date($Ebirth_date)
})
"""