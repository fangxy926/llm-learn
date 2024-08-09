class ColumnInfo:
    def __init__(self, columnID, columnName, dataType, dataDefault, dataLength, dataPrecision, dataScale, nullAble,
                 comments, constraintType, chinese):
        self.columnID = columnID
        self.columnName = columnName
        self.dataType = dataType
        self.dataDefault = dataDefault
        self.dataLength = dataLength
        self.dataPrecision = dataPrecision
        self.dataScale = dataScale
        self.nullAble = nullAble
        self.comments = comments
        self.constraintType = constraintType
        self.chinese = chinese

    def __repr__(self):
        return f"ColumnInfo(columnID={self.columnID}, columnName='{self.columnName}', dataType='{self.dataType}', dataDefault={self.dataDefault}, dataLength={self.dataLength}, dataPrecision={self.dataPrecision}, dataScale={self.dataScale}, nullAble='{self.nullAble}', comments='{self.comments}', constraintType='{self.constraintType}', chinese='{self.chinese}')"
