import lombok.Data;
import java.io.Serializable;
import java.util.Date;
import com.baomidou.mybatisplus.annotation.KeySequence;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.github.jeffreyning.mybatisplus.anno.MppMultiId;

@Data
@TableName(value = "xtgl_rjkf_bdys")
@KeySequence(value = "")
public class XtglRjkfBdysPo implements Serializable {

    /**
     *  表单元素ID
     */
    @TableId(value = "yuansuid")
    private Long yuanSUID;

    /**
     *  表单ID
     */
    @TableField(value = "biaodanid")
    private Integer biaoDanID;

    /**
     *  元素名称
     */
    @TableField(value = "mingcheng")
    private String mingCheng;

    /**
     *  数据类型: 1字符型; 2数值型; 3日期型
     */
    @TableField(value = "shujulx")
    private String shuJuLX;

    /**
     *  是否非空: 0否 1是
     */
    @TableField(value = "feikong")
    private String feiKong;

    /**
     *  是否唯一: 0否 1是
     */
    @TableField(value = "weiyi")
    private String weiYi;

    /**
     *  默认值
     */
    @TableField(value = "morenzhi")
    private String moRenZhi;

    /**
     *  格式
     */
    @TableField(value = "geshi")
    private String geShi;

    /**
     *  最小长度
     */
    @TableField(value = "zuixiaocd")
    private Integer zuiXiaoCD;

    /**
     *  最大长度
     */
    @TableField(value = "zuidacd")
    private Integer zuiDaCD;

    /**
     *  最小值
     */
    @TableField(value = "zuixiaozhi")
    private BigDecimal zuiXiaoZhi;

    /**
     *  最大值
     */
    @TableField(value = "zuidazhi")
    private BigDecimal zuiDaZhi;

    /**
     *  备注
     */
    @TableField(value = "beizu")
    private String beiZu;

    /**
     *  值域类型: 1手动输入; 2接口数据
     */
    @TableField(value = "zhiyulx")
    private String zhiYuLX;

    /**
     *  排序
     */
    @TableField(value = "paixu")
    private Integer paiXu;

    /**
     *  操作者ID
     */
    @TableField(value = "caozuozheid")
    private Integer caoZuoZheID;

    /**
     *  操作者姓名
     */
    @TableField(value = "caozuozhexm")
    private String caoZuoZheXM;

    /**
     *  操作时间
     */
    @TableField(value = "caozuosj")
    private Date caoZuoSJ;

    /**
     *  是否可编辑（默认是）
     */
    @TableField(value = "kebianji")
    private String keBianJi;
}
